
from django.urls import path

from estacionamiento.views import (
    estancia_lista,
    estancia_crear,
    estancia_detalle,
    estancia_editar,
    estancia_eliminar,
    estancia_salida
)


urlpatterns = [
    path('estancias/', estancia_lista, name='estancia_lista'),
    path('estancias/crear/', estancia_crear, name='estancia_crear'),
    path('estancias/<int:pk>/', estancia_detalle, name='estancia_detalle'),
    path('estancias/<int:pk>/editar/', estancia_editar, name='estancia_editar'),
    path('estancias/<int:pk>/eliminar/', estancia_eliminar, name='estancia_eliminar'),
    path('estancias/<int:pk>/salida/', estancia_salida, name='estancia_salida'),
]
