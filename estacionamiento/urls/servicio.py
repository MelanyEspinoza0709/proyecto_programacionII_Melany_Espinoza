from django.urls import path
from estacionamiento.views import (
    servicio_lista,
    servicio_detalle
)


urlpatterns = [
    path('servicios/', servicio_lista, name='servicio_lista'),
    path('servicios/<int:pk>/', servicio_detalle, name='servicio_detalle'),
]