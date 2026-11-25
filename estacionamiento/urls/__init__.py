from django.urls import path

from .cliente import urlpatterns as cliente_urls
from .vehiculo import urlpatterns as vehiculo_urls
from .estancia import urlpatterns as estancia_urls
from .servicio import urlpatterns as servicio_urls
from .espacio import urlpatterns as espacio_urls
from .auth import urlpatterns as auth_urls

from estacionamiento.views.auth_views import inicio

app_name = 'estacionamiento'

urlpatterns = [
    path('', inicio, name='inicio'),
] + (
    cliente_urls +
    vehiculo_urls +
    estancia_urls +
    servicio_urls +
    espacio_urls +
    auth_urls
)
