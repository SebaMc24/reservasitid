from django.db import models
from django.utils import timezone
from datetime import timedelta

class Sala(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    capacidad_maxima = models.PositiveIntegerField()
    habilitada = models.BooleanField(default=True, verbose_name="Habilitada")

    def __str__(self):
        return self.nombre

    @property
    def disponible(self):
        return self.habilitada and not self.reservas.filter(
            fecha_termino__gt=timezone.now()
        ).exists()

class Reserva(models.Model):
    rut = models.CharField(max_length=12)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_termino = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.fecha_termino = self.fecha_inicio + timedelta(hours=2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rut} - {self.sala}"