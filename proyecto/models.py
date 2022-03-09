from django.db import models

# Create your models here.
class UsuarioBase(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)

class Cliente(UsuarioBase):
    idC = models.AutoField(primary_key=True)
    saldo = models.PositiveIntegerField()
    telefono = models.PositiveIntegerField()
    imagen = models.ImageField()

class Empresa(UsuarioBase):
    idEm = models.AutoField(primary_key=True)
    telefonoEmpresa = models.PositiveIntegerField()
    imagenEmpresa = models.ImageField()

class Empleado(UsuarioBase):
    idE = models.AutoField(primary_key=True)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    totalEntradas = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100)
    codigoQR = models.CharField(max_length=100)
    descripcion = models.TextField()
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Entrada(models.Model):
    id = models.AutoField(primary_key=True)
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
    ubicacion = models.CharField(max_length=100)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    idEvento = models.ForeignKey(Evento, on_delete=models.CASCADE)
