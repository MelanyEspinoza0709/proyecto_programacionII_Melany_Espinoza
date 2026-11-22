from django.db import models
from django.urls import reverse
from .cliente import Cliente

class Vehiculo(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='vehiculos'
    )
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    placa = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=30)

    class Meta:
        ordering = ['marca', 'modelo']
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"
    def get_absolute_url(self):
        return reverse('estacionamiento:vehiculo_detalle', kwargs={'pk': self.pk})
