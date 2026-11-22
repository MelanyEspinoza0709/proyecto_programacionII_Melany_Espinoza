from django.contrib import admin
from .models import Cliente, Vehiculo, Estancia, Servicio


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'telefono', 'correo')
    search_fields = ('nombre', 'apellido', 'cedula')
    ordering = ('apellido',)


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'placa', 'color', 'cliente')
    search_fields = ('marca', 'modelo', 'placa')
    list_filter = ('marca',)


@admin.register(Estancia)
class EstanciaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'espacio', 'fecha_entrada', 'fecha_salida', 'total', 'estado', 'creado_por')
    search_fields = ('espacio', 'vehiculo__placa')
    list_filter = ('estado',)


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)