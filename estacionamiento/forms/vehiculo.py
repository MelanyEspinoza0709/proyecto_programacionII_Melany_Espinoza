from django import forms
from estacionamiento.models import Vehiculo


class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = [
            'cliente',
            'marca',
            'modelo',
            'anio',
            'placa',
            'color'
        ]

        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
        }