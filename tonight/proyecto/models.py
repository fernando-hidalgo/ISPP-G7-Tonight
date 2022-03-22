from distutils.command.upload import upload
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

import datetime
# Create your models here.

class Cliente(models.Model):
    user = models.OneToOneField(User, related_name='user_c', on_delete=models.CASCADE)
    saldo = models.PositiveIntegerField()
    tlf = models.PositiveIntegerField()
    imagen = models.ImageField(blank=True, upload_to='media/')

class Empresa(models.Model):
    user = models.OneToOneField(User, related_name='user_eprs', on_delete=models.CASCADE)
    tlf = models.PositiveIntegerField()
    imagen = models.ImageField(blank=True, upload_to='media/')

class Empleado(models.Model):
    user = models.OneToOneField(User, related_name='user_epld', on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Evento(models.Model):
    fecha = models.DateTimeField()
    precioEntrada = models.PositiveIntegerField()
    totalEntradas = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500)
    ubicacion = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa')
    imagen = models.ImageField(blank=True, upload_to='media/')

class Entrada(models.Model):
    fechaCompra = models.DateTimeField()
    fechaCaducidad = models.DateTimeField()
    STATUS = (
        ('E', 'En venta'),
        ('A', 'Adquirida'),
        ('V', 'Vendida'),
        ('U','Usada'),
        ('C', 'Caducada')
    )
    estado = models.CharField(max_length=1, choices=STATUS)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cliente')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='evento')
    hash = models.CharField(max_length=100, blank=True)
