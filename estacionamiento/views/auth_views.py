from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.views.decorators.http import require_POST

from estacionamiento.forms import RegistroForm


def registro(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)

        if formulario.is_valid():
            usuario = formulario.save()

            recepcionistas, creado = Group.objects.get_or_create(
                name='Recepcionistas'
            )

            usuario.groups.add(recepcionistas)

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


def iniciar_sesion(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request, data=request.POST)

        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            messages.success(request, 'Bienvenido a Luxury Parking.')
            return redirect('estacionamiento:cliente_lista')
    else:
        formulario = AuthenticationForm()

    return render(
        request,
        'estacionamiento/autenticacion/login.html',
        {'formulario': formulario}
    )


@require_POST
def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('estacionamiento:login')
