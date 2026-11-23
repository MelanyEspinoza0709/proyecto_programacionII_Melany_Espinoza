from .cliente import urlpatterns as cliente_urls
from .vehiculo import urlpatterns as vehiculo_urls
from .estancia import urlpatterns as estancia_urls
from .servicio import urlpatterns as servicio_urls

app_name = 'estacionamiento'

urlpatterns = (
    cliente_urls +
    vehiculo_urls +
    estancia_urls +
    servicio_urls
)