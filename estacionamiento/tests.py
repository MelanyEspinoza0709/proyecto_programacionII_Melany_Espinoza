
import re
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User, Group, Permission
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from estacionamiento.models import Cliente, Estancia, Servicio, Vehiculo


class AutenticacionTest(TestCase):

    def test_login_muestra_pagina(self):
        respuesta = self.client.get(reverse('estacionamiento:login'))

        self.assertEqual(respuesta.status_code, 200)

    def test_registro_muestra_pagina(self):
        respuesta = self.client.get(reverse('estacionamiento:registro'))

        self.assertEqual(respuesta.status_code, 200)


class PermisosTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='recepcionista',
            password='Prueba12345'
        )

        self.grupo, creado = Group.objects.get_or_create(
            name='Recepcionistas'
        )

        permisos = Permission.objects.filter(
            content_type__app_label='estacionamiento',
            codename__in=[
                'view_cliente',
                'add_cliente',
                'change_cliente'
            ]
        )

        self.grupo.permissions.set(permisos)
        self.usuario.groups.add(self.grupo)

    def test_usuario_no_autenticado_no_ve_clientes(self):
        respuesta = self.client.get(
            reverse('estacionamiento:cliente_lista')
        )

        self.assertEqual(respuesta.status_code, 302)

    def test_recepcionista_puede_ver_clientes(self):
        self.client.login(
            username='recepcionista',
            password='Prueba12345'
        )

        respuesta = self.client.get(
            reverse('estacionamiento:cliente_lista')
        )

        self.assertEqual(respuesta.status_code, 200)


class EstanciaSalidaTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='recepcionista_estancias',
            password='Prueba12345'
        )
        permisos = Permission.objects.filter(
            content_type__app_label='estacionamiento',
            codename__in=[
                'add_estancia',
                'change_estancia',
                'view_estancia'
            ]
        )
        self.usuario.user_permissions.set(permisos)
        self.client.force_login(self.usuario)

        cliente = Cliente.objects.create(
            nombre='Ana',
            apellido='Pérez',
            cedula='1234567890',
            telefono='0991234567',
            correo='ana@example.com'
        )
        self.vehiculo = Vehiculo.objects.create(
            cliente=cliente,
            marca='Toyota',
            modelo='Corolla',
            anio=2020,
            placa='ABC1234',
            color='Gris'
        )
        self.servicio_lavado = Servicio.objects.create(
            nombre='Lavado',
            descripcion='Lavado exterior',
            precio=Decimal('10.00')
        )
        self.servicio_cera = Servicio.objects.create(
            nombre='Cera',
            descripcion='Aplicación de cera',
            precio=Decimal('5.00')
        )

    def test_crear_estancia_y_registrar_salida_con_servicios_y_csrf(self):
        formulario_url = reverse('estacionamiento:estancia_crear')
        respuesta = self.client.get(formulario_url)
        self.assertContains(respuesta, 'Lavado - $10.00')
        self.assertContains(respuesta, 'Cera - $5.00')

        entrada = timezone.localtime(
            timezone.now() - timedelta(hours=2, minutes=20)
        )
        respuesta = self.client.post(formulario_url, {
            'vehiculo': self.vehiculo.pk,
            'servicios': [self.servicio_lavado.pk, self.servicio_cera.pk],
            'espacio': 'A1',
            'fecha_entrada': entrada.strftime('%Y-%m-%dT%H:%M'),
            'fecha_salida': '',
            'estado': Estancia.Estado.ACTIVA,
        })
        self.assertRedirects(
            respuesta,
            reverse('estacionamiento:estancia_lista')
        )

        estancia = Estancia.objects.get()
        self.assertEqual(estancia.estado, Estancia.Estado.ACTIVA)
        self.assertEqual(
            set(estancia.servicios.values_list('pk', flat=True)),
            {self.servicio_lavado.pk, self.servicio_cera.pk}
        )

        cliente_csrf = Client(enforce_csrf_checks=True)
        cliente_csrf.force_login(self.usuario)
        listado_url = reverse('estacionamiento:estancia_lista')
        listado = cliente_csrf.get(listado_url)
        self.assertContains(listado, 'Registrar salida')

        token = re.search(
            rb'name="csrfmiddlewaretoken" value="([^"]+)"',
            listado.content
        ).group(1).decode()
        salida_url = reverse(
            'estacionamiento:estancia_salida',
            kwargs={'pk': estancia.pk}
        )
        self.assertEqual(
            cliente_csrf.post(salida_url).status_code,
            403
        )
        respuesta = cliente_csrf.post(
            salida_url,
            {'csrfmiddlewaretoken': token}
        )
        self.assertRedirects(respuesta, listado_url)

        estancia.refresh_from_db()
        self.assertEqual(estancia.estado, Estancia.Estado.FINALIZADA)
        self.assertEqual(estancia.total, Decimal('21.00'))
        self.assertIsNotNone(estancia.fecha_salida)

        listado_final = cliente_csrf.get(listado_url)
        self.assertContains(listado_final, 'FINALIZADA')
        self.assertContains(listado_final, '$21,00')
        self.assertNotContains(listado_final, 'Registrar salida')

        fecha_salida = estancia.fecha_salida
        cliente_csrf.post(
            salida_url,
            {'csrfmiddlewaretoken': token}
        )
        estancia.refresh_from_db()
        self.assertEqual(estancia.estado, Estancia.Estado.FINALIZADA)
        self.assertEqual(estancia.total, Decimal('21.00'))
        self.assertEqual(estancia.fecha_salida, fecha_salida)
