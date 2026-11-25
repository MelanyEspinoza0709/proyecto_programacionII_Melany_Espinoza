from datetime import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from estacionamiento.models import Cliente, Vehiculo, Estancia, Servicio


class Command(BaseCommand):
    help = 'Crear datos de prueba para Luxury Parking'

    @transaction.atomic
    def handle(self, *args, **kwargs):

        # Crear usuario para registrar las estancias
        usuario, creado = User.objects.get_or_create(
            username='usuario_datos_demo',
            defaults={
                'email': 'demo@luxuryparking.com'
            }
        )

        if creado:
            usuario.set_unusable_password()
            usuario.save()

        # Crear clientes
        datos_clientes = [
            ('Carlos', 'Mendoza', '1700000001', '0991111111', 'carlos@gmail.com'),
            ('Ana', 'Torres', '1700000002', '0992222222', 'ana@gmail.com'),
            ('Luis', 'Ramirez', '1700000003', '0993333333', 'luis@gmail.com'),
            ('Maria', 'Castro', '1700000004', '0994444444', 'maria@gmail.com'),
            ('Pedro', 'Vargas', '1700000005', '0995555555', 'pedro@gmail.com'),
        ]

        clientes = []

        for nombre, apellido, cedula, telefono, correo in datos_clientes:
            cliente, creado = Cliente.objects.get_or_create(
                cedula=cedula,
                defaults={
                    'nombre': nombre,
                    'apellido': apellido,
                    'telefono': telefono,
                    'correo': correo
                }
            )
            clientes.append(cliente)

        # Crear vehículos
        datos_vehiculos = [
            ('Toyota', 'Corolla', 2022, 'LP-DEMO-01', 'Blanco'),
            ('Chevrolet', 'Onix', 2023, 'LP-DEMO-02', 'Negro'),
            ('Hyundai', 'Tucson', 2021, 'LP-DEMO-03', 'Gris'),
            ('Kia', 'Sportage', 2024, 'LP-DEMO-04', 'Rojo'),
            ('Mazda', 'CX5', 2022, 'LP-DEMO-05', 'Azul'),
        ]

        vehiculos = []

        for i, datos in enumerate(datos_vehiculos):
            marca, modelo, anio, placa, color = datos

            vehiculo, creado = Vehiculo.objects.get_or_create(
                placa=placa,
                defaults={
                    'cliente': clientes[i],
                    'marca': marca,
                    'modelo': modelo,
                    'anio': anio,
                    'color': color
                }
            )
            vehiculos.append(vehiculo)

        # Crear estancias
        datos_estancias = [
            ('A01', 20, 'ACTIVA', '0.00'),
            ('A02', 21, 'FINALIZADA', '5.00'),
            ('A03', 22, 'FINALIZADA', '8.50'),
            ('B01', 23, 'CANCELADA', '0.00'),
            ('B02', 24, 'ACTIVA', '0.00'),
        ]

        estancias = []

        for i, datos in enumerate(datos_estancias):
            espacio, dia, estado, total = datos

            fecha = timezone.make_aware(
                datetime(2026, 11, dia, 8, 0)
            )

            estancia, creado = Estancia.objects.get_or_create(
                vehiculo=vehiculos[i],
                espacio=espacio,
                fecha_entrada=fecha,
                defaults={
                    'creado_por': usuario,
                    'fecha_salida': None,
                    'total': total,
                    'estado': estado
                }
            )
            estancias.append(estancia)

        # Crear servicios
        datos_servicios = [
            ('Lavado básico', 'Lavado exterior del vehículo.', '5.00'),
            ('Lavado completo', 'Lavado interior y exterior.', '10.00'),
            ('Encerado', 'Aplicación de cera para proteger la pintura.', '8.00'),
            ('Aspirado', 'Limpieza interior mediante aspirado.', '4.00'),
            ('Pulido', 'Pulido de la carrocería del vehículo.', '15.00'),
        ]

        servicios = []

        for nombre, descripcion, precio in datos_servicios:
            servicio, creado = Servicio.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': descripcion,
                    'precio': precio
                }
            )
            servicios.append(servicio)

        # Relacionar servicios con estancias
        for i in range(5):
            servicios[i].estancias.add(estancias[i])

        self.stdout.write(
            self.style.SUCCESS(
                '¡Datos de prueba creados correctamente!'
            )
        )

        self.stdout.write(f'Clientes: {Cliente.objects.count()}')
        self.stdout.write(f'Vehículos: {Vehiculo.objects.count()}')
        self.stdout.write(f'Estancias: {Estancia.objects.count()}')
        self.stdout.write(f'Servicios: {Servicio.objects.count()}')
