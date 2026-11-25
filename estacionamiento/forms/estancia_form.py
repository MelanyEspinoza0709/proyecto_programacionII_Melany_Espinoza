
from django import forms
from estacionamiento.models import Estancia, Servicio


class EstanciaForm(forms.ModelForm):

    servicios = forms.ModelMultipleChoiceField(
        queryset=Servicio.objects.all().order_by('nombre'),
        required=False,
        label='Servicios solicitados',
        widget=forms.CheckboxSelectMultiple,
        help_text='Selecciona los servicios que solicita el cliente.'
    )

    class Meta:
        model = Estancia
        fields = [
            'vehiculo',
            'servicios',
            'espacio',
            'fecha_entrada',
            'fecha_salida',
            'estado'
        ]

        widgets = {
            'vehiculo': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'espacio': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'fecha_entrada': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            'fecha_salida': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            'estado': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['servicios'].label_from_instance = (
            lambda servicio: f"{servicio.nombre} - ${servicio.precio:.2f}"
        )

    def save(self, commit=True):
        estancia = super().save(commit=commit)

        if commit:
            estancia.servicios.set(self.cleaned_data['servicios'])
        else:
            guardar_m2m_original = self.save_m2m

            def guardar_m2m():
                guardar_m2m_original()
                estancia.servicios.set(self.cleaned_data['servicios'])

            self.save_m2m = guardar_m2m

        return estancia
