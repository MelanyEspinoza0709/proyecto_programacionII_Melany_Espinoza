
import math
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from estacionamiento.models import Estancia
from estacionamiento.forms import EstanciaForm


# Listar estancias
@login_required
@permission_required('estacionamiento.view_estancia', raise_exception=True)
def estancia_lista(request):
    estancias = Estancia.objects.all()

    return render(request, 'estacionamiento/estancias/lista.html', {
        'estancias': estancias
    })


# Registrar estancia
@login_required
@permission_required('estacionamiento.add_estancia', raise_exception=True)
def estancia_crear(request):
    if request.method == 'POST':
        formulario = EstanciaForm(request.POST)

        if formulario.is_valid():
            estancia = formulario.save(commit=False)
            estancia.creado_por = request.user
            estancia.estado = Estancia.Estado.ACTIVA
            estancia.fecha_salida = None
            estancia.total = Decimal('0.00')
            estancia.save()
            formulario.save_m2m()

            messages.success(request, 'Estancia registrada correctamente.')
            return redirect('estacionamiento:estancia_lista')

    else:
        formulario = EstanciaForm()

    return render(request, 'estacionamiento/estancias/formulario.html', {
        'formulario': formulario
    })


# Ver detalles
@login_required
@permission_required('estacionamiento.view_estancia', raise_exception=True)
def estancia_detalle(request, pk):
    estancia = get_object_or_404(Estancia, pk=pk)

    return render(request, 'estacionamiento/estancias/detalle.html', {
        'estancia': estancia
    })


# Editar estancia
@login_required
@permission_required('estacionamiento.change_estancia', raise_exception=True)
def estancia_editar(request, pk):
    estancia = get_object_or_404(Estancia, pk=pk)

    if not request.user.is_superuser and estancia.creado_por != request.user:
        raise PermissionDenied

    if estancia.estado == Estancia.Estado.FINALIZADA:
        messages.error(request, 'No puedes editar una estancia finalizada.')
        return redirect('estacionamiento:estancia_lista')

    if request.method == 'POST':
        formulario = EstanciaForm(request.POST, instance=estancia)

        if formulario.is_valid():
            estancia = formulario.save(commit=False)
            estancia.estado = Estancia.Estado.ACTIVA
            estancia.fecha_salida = None
            estancia.total = Decimal('0.00')
            estancia.save()
            formulario.save_m2m()

            messages.success(request, 'Estancia actualizada correctamente.')
            return redirect('estacionamiento:estancia_lista')

    else:
        formulario = EstanciaForm(instance=estancia)

    return render(request, 'estacionamiento/estancias/formulario.html', {
        'formulario': formulario,
        'estancia': estancia
    })


# Registrar salida y calcular total
@login_required
@permission_required('estacionamiento.change_estancia', raise_exception=True)
def estancia_salida(request, pk):
    estancia = get_object_or_404(Estancia, pk=pk)

    if not request.user.is_superuser and estancia.creado_por != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        if estancia.estado != Estancia.Estado.ACTIVA:
            messages.error(request, 'Esta estancia ya no está activa.')
            return redirect('estacionamiento:estancia_lista')

        fecha_salida = timezone.now()

        duracion = fecha_salida - estancia.fecha_entrada
        horas = max(1, math.ceil(duracion.total_seconds() / 3600))

        precio_hora = Decimal('2.00')
        precio_estacionamiento = precio_hora * horas

        precio_servicios = sum(
            estancia.servicios.values_list('precio', flat=True),
            Decimal('0.00')
        )

        estancia.fecha_salida = fecha_salida
        estancia.total = precio_estacionamiento + precio_servicios
        estancia.estado = Estancia.Estado.FINALIZADA
        estancia.save()

        messages.success(
            request,
            f'Estancia finalizada. Total a cobrar: ${estancia.total:.2f}'
        )

    return redirect('estacionamiento:estancia_lista')


# Eliminar estancia
@login_required
@permission_required('estacionamiento.delete_estancia', raise_exception=True)
def estancia_eliminar(request, pk):
    estancia = get_object_or_404(Estancia, pk=pk)

    if not request.user.is_superuser and estancia.creado_por != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        estancia.delete()
        messages.success(request, 'Estancia eliminada correctamente.')
        return redirect('estacionamiento:estancia_lista')

    return render(request, 'estacionamiento/estancias/confirmar_eliminar.html', {
        'estancia': estancia
    })
