from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required

from estacionamiento.models import Estancia


# Listar espacios
@login_required
@permission_required('estacionamiento.view_estancia', raise_exception=True)
def espacio_lista(request):
    espacios = Estancia.objects.values('espacio').distinct().order_by('espacio')

    return render(
        request,
        'estacionamiento/espacios/lista.html',
        {'espacios': espacios}
    )


# Ver detalles del espacio
@login_required
@permission_required('estacionamiento.view_estancia', raise_exception=True)
def espacio_detalle(request, espacio):
    estancias = Estancia.objects.filter(
        espacio=espacio
    ).order_by('-fecha_entrada')

    if not estancias.exists():
        raise Http404("El espacio no existe.")

    ocupado = estancias.filter(estado='ACTIVA').exists()

    return render(
        request,
        'estacionamiento/espacios/detalle.html',
        {
            'espacio': espacio,
            'estancias': estancias,
            'ocupado': ocupado
        }
    )
