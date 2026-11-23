from django.urls import path
from estacionamiento.views import (
    cliente_lista,
    cliente_crear,
    cliente_detalle,
    cliente_editar,
    cliente_eliminar
)

urlpatterns = [
    path('clientes/', cliente_lista, name='cliente_lista'),
    path('clientes/crear/', cliente_crear, name='cliente_crear'),
    path('clientes/<int:pk>/', cliente_detalle, name='cliente_detalle'),
    path('clientes/<int:pk>/editar/', cliente_editar, name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', cliente_eliminar, name='cliente_eliminar'),
]