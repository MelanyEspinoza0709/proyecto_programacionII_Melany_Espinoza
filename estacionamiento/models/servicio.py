from django.db import models
from django.urls import reverse

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    estancias = models.ManyToManyField(
        'Estancia',
        related_name='servicios',
        blank=True
    )

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('estacionamiento:servicio_detalle', kwargs={'pk': self.pk})
