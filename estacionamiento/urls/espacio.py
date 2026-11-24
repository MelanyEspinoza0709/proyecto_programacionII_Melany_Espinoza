
from django.urls import path
from estacionamiento.views.espacio import espacio_lista, espacio_detalle

urlpatterns = [
    path('espacios/', espacio_lista, name='espacio_lista'),
    path('espacios/<str:espacio>/', espacio_detalle, name='espacio_detalle'),
]
