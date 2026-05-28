from django.db import models
from django.contrib.auth.models import User


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    ubicacion = models.CharField(max_length=255)
    capacidad = models.IntegerField()
    cupos_disponibles = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Reservacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fecha_reservacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default="ACTIVA")

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.nombre}"