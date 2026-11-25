
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission


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
