from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied

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

    if request.method == 'POST':
        formulario = EstanciaForm(request.POST, instance=estancia)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Estancia actualizada correctamente.')
            return redirect('estacionamiento:estancia_lista')

    else:
        formulario = EstanciaForm(instance=estancia)

    return render(request, 'estacionamiento/estancias/formulario.html', {
        'formulario': formulario,
        'estancia': estancia
    })


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
