
from django.shortcuts import render, get_object_or_404

from estacionamiento.models import Estancia


def espacio_lista(request):
    espacios = Estancia.objects.values('espacio').distinct().order_by('espacio')

    return render(
        request,
        'estacionamiento/espacios/lista.html',
        {'espacios': espacios}
    )


def espacio_detalle(request, espacio):
    estancias = Estancia.objects.filter(espacio=espacio).order_by('-fecha_entrada')

    if not estancias.exists():
        from django.http import Http404
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
