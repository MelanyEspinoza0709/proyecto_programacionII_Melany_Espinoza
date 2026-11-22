from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .vehiculo import Vehiculo

class Estancia(models.Model):
    class Estado(models.TextChoices):
        ACTIVA = 'ACTIVA', 'Activa'
        FINALIZADA = 'FINALIZADA', 'Finalizada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT,
        related_name='estancias'
    )
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='estancias_registradas'
    )

    espacio = models.CharField(max_length=20)
    fecha_entrada = models.DateTimeField()
    fecha_salida = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.ACTIVA
    )
    class Meta:
        ordering = ['-fecha_entrada']
        verbose_name = 'Estancia'
        verbose_name_plural = 'Estancias'

    def __str__(self):
        return f"{self.vehiculo} - {self.get_estado_display()}"

    def get_absolute_url(self):
        return reverse('estacionamiento:estancia_detalle', kwargs={'pk': self.pk})
