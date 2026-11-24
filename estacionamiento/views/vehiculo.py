
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from estacionamiento.models import Vehiculo
from estacionamiento.forms import VehiculoForm


# Listar vehículos
@login_required
def vehiculo_lista(request):
    vehiculos = Vehiculo.objects.all()

    return render(request, 'estacionamiento/vehiculos/lista.html', {
        'vehiculos': vehiculos
    })


# Registrar vehículo
@login_required
def vehiculo_crear(request):
    if request.method == 'POST':
        formulario = VehiculoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Vehículo registrado correctamente.')
            return redirect('estacionamiento:vehiculo_lista')

    else:
        formulario = VehiculoForm()

    return render(request, 'estacionamiento/vehiculos/formulario.html', {
        'formulario': formulario
    })


# Ver detalles
@login_required
def vehiculo_detalle(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    return render(request, 'estacionamiento/vehiculos/detalle.html', {
        'vehiculo': vehiculo
    })


# Editar vehículo
@login_required
def vehiculo_editar(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == 'POST':
        formulario = VehiculoForm(request.POST, instance=vehiculo)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Vehículo actualizado correctamente.')
            return redirect('estacionamiento:vehiculo_lista')

    else:
        formulario = VehiculoForm(instance=vehiculo)

    return render(request, 'estacionamiento/vehiculos/formulario.html', {
        'formulario': formulario,
        'vehiculo': vehiculo
    })


# Eliminar vehículo
@login_required
def vehiculo_eliminar(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado correctamente.')
        return redirect('estacionamiento:vehiculo_lista')

    return render(request, 'estacionamiento/vehiculos/confirmar_eliminar.html', {
        'vehiculo': vehiculo
    })
