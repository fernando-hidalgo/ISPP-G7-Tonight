from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db import models
from pyexpat import model
from distutils.command.upload import upload

import datetime
# Create your models here.

class Cliente(models.Model):
    user = models.OneToOneField(User, related_name='user_c', on_delete=models.CASCADE)
    saldo = models.PositiveIntegerField()
    tlf = PhoneNumberField(unique = True)
    imagen = models.ImageField(blank=True, upload_to='media/')

class Empresa(models.Model):
    user = models.OneToOneField(User, related_name='user_eprs', on_delete=models.CASCADE)
    tlf = models.PositiveIntegerField()
    imagen = models.ImageField(blank=True, upload_to='media/')

class Empleado(models.Model):
    user = models.OneToOneField(User, related_name='user_epld', on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Evento(models.Model):
    fecha = models.DateTimeField('Fecha', validators=[MinValueValidator(timezone.now() + timezone.timedelta(days=1))])
    precioEntrada = models.PositiveIntegerField('Precio Entrada')
    totalEntradas = models.PositiveIntegerField('Total Entradas')
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción', max_length=500)
    ubicacion = models.CharField('Ubicación', max_length=100)
    salt = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa')
    imagen = models.ImageField('Imagen',blank=True, upload_to='media/')

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

class Transaccion(models.Model):
    TYPE = (
        ('V', 'Vender'),
        ('C', 'Comprar'),
    )
    tipo = models.CharField(max_length=1, choices=TYPE)
    fechaAudit = models.DateTimeField()
    fechaLimite = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cliente_trans')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='evento_trans', blank=True)
    done = models.BooleanField(default=False)