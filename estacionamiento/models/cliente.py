from django.db import models
from django.urls import reverse

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(blank=True)

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def get_absolute_url(self):
        return reverse('estacionamiento:cliente_detalle', kwargs={'pk': self.pk})
