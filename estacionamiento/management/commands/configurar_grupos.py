
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Crear los grupos y asignar sus permisos'

    def handle(self, *args, **kwargs):

        administradores, creado = Group.objects.get_or_create(
            name='Administradores'
        )

        recepcionistas, creado = Group.objects.get_or_create(
            name='Recepcionistas'
        )

        modelos = [
            'cliente',
            'vehiculo',
            'estancia',
            'servicio',
        ]

        permisos_administradores = Permission.objects.filter(
            content_type__app_label='estacionamiento',
            content_type__model__in=modelos
        )

        administradores.permissions.set(permisos_administradores)

        permisos_recepcionistas = Permission.objects.filter(
            content_type__app_label='estacionamiento',
            content_type__model__in=modelos,
            codename__in=[
                'view_cliente', 'add_cliente', 'change_cliente',
                'view_vehiculo', 'add_vehiculo', 'change_vehiculo',
                'view_estancia', 'add_estancia', 'change_estancia',
                'view_servicio', 'add_servicio', 'change_servicio',
            ]
        )

        recepcionistas.permissions.set(permisos_recepcionistas)

        self.stdout.write(
            self.style.SUCCESS('Grupos y permisos creados correctamente.')
        )
