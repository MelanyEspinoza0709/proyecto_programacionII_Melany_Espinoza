from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from estacionamiento.models import Cliente
from estacionamiento.forms import ClienteForm

def cliente_lista(request):
    clientes = Cliente.objects.all()

    return render(request, 'estacionamiento/clientes/lista.html', {
        'clientes': clientes
    })

def cliente_crear(request):
    if request.method == 'POST':
        formulario = ClienteForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cliente registrado correctamente.')
            return redirect('estacionamiento:cliente_lista')

    else:
        formulario = ClienteForm()

    return render(request, 'estacionamiento/clientes/formulario.html', {
        'formulario': formulario
    })

def cliente_detalle(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    return render(request, 'estacionamiento/clientes/detalle.html', {
        'cliente': cliente
    })

def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        formulario = ClienteForm(request.POST, instance=cliente)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('estacionamiento:cliente_lista')

    else:
        formulario = ClienteForm(instance=cliente)

    return render(request, 'estacionamiento/clientes/formulario.html', {
        'formulario': formulario,
        'cliente': cliente
    })


def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('estacionamiento:cliente_lista')

    return render(request, 'estacionamiento/clientes/confirmar_eliminar.html', {
        'cliente': cliente
    })