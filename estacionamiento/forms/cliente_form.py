from django import forms
from estacionamiento.models import Cliente


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'apellido',
            'cedula',
            'telefono',
            'correo'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')

        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError(
                'La cédula debe contener exactamente 10 números.'
            )

        return cedula