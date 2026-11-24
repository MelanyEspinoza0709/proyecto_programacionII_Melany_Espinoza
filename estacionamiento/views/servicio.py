
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from estacionamiento.models import Servicio


@login_required
def servicio_lista(request):
    servicios = Servicio.objects.all()

    return render(request, 'estacionamiento/servicios/lista.html', {
        'servicios': servicios
    })


@login_required
def servicio_detalle(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)

    return render(request, 'estacionamiento/servicios/detalle.html', {
        'servicio': servicio
    })
