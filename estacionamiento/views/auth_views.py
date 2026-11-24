
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from estacionamiento.forms import RegistroForm


def registro(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)

        if formulario.is_valid():
            usuario = formulario.save()
            login(request, usuario)
            messages.success(request, 'Tu cuenta fue creada correctamente.')
            return redirect('estacionamiento:cliente_lista')
    else:
        formulario = RegistroForm()

    return render(
        request,
        'estacionamiento/autenticacion/registro.html',
        {'formulario': formulario}
    )
