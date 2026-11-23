from django.urls import path
from estacionamiento.views import (
    vehiculo_lista,
    vehiculo_crear,
    vehiculo_detalle,
    vehiculo_editar,
    vehiculo_eliminar
)


urlpatterns = [
    path('vehiculos/', vehiculo_lista, name='vehiculo_lista'),
    path('vehiculos/crear/', vehiculo_crear, name='vehiculo_crear'),
    path('vehiculos/<int:pk>/', vehiculo_detalle, name='vehiculo_detalle'),
    path('vehiculos/<int:pk>/editar/', vehiculo_editar, name='vehiculo_editar'),
    path('vehiculos/<int:pk>/eliminar/', vehiculo_eliminar, name='vehiculo_eliminar'),
]
