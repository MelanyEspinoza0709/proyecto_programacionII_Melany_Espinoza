from django.shortcuts import render, get_object_or_404
from estacionamiento.models import Servicio

def servicio_lista(request):
    servicios = Servicio.objects.all()

    return render(request, 'estacionamiento/servicios/lista.html', {
        'servicios': servicios
    })

def servicio_detalle(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)

    return render(request, 'estacionamiento/servicios/detalle.html', {
        'servicio': servicio
    })
    