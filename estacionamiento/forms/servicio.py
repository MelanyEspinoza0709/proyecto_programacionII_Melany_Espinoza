from django import forms
from estacionamiento.models import Servicio


class ServicioForm(forms.ModelForm):

    class Meta:
        model = Servicio
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'estancias'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estancias': forms.CheckboxSelectMultiple(),
        }