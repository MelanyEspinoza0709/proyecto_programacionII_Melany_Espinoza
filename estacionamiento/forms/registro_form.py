
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):

    username = forms.CharField(
        label='Nombre de usuario',
        help_text='Escribe un nombre para ingresar al sistema.'
    )

    email = forms.EmailField(
        required=True,
        label='Correo electrónico'
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text='La contraseña debe ser segura.'
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput,
        help_text='Escribe nuevamente tu contraseña.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
