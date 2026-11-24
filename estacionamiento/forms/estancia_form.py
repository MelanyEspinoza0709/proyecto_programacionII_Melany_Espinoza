from django import forms
from estacionamiento.models import Estancia


class EstanciaForm(forms.ModelForm):

    class Meta:
        model = Estancia
        fields = [
            'vehiculo',
            'espacio',
            'fecha_entrada',
            'fecha_salida',
            'total',
            'estado'
        ]

        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'espacio': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_entrada': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'fecha_salida': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'total': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }