from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from estacionamiento.models import Servicio


# Listar servicios
@login_required
@permission_required('estacionamiento.view_servicio', raise_exception=True)
def servicio_lista(request):
    servicios = Servicio.objects.all()

    return render(request, 'estacionamiento/servicios/lista.html', {
        'servicios': servicios
    })


# Ver detalles
@login_required
@permission_required('estacionamiento.view_servicio', raise_exception=True)
def servicio_detalle(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)

    return render(request, 'estacionamiento/servicios/detalle.html', {
        'servicio': servicio
    })
