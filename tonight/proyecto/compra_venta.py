from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from tonight.proyecto.models import Cliente, Entrada, Evento

# asignamos una entrada disponible a un usuario
def venderEntradas(request, nombre_evento):
    evento_ = Evento.objects.get(nombre=nombre_evento) # evento del que queremos entrada
    usuario = request.user # usuario que compra la entrada
    entradas = Entrada.objects.filter(evento=evento_).all() # conjunto de todas las entradas
    entrada_disponible = entradas.filter(estado='E')
    #modificamos los valores de la entrada a vender
    entrada_disponible.fechaCompra=datetime.today
    entrada_disponible.estado='V'
    entrada_disponible.cliente=usuario
    # guardamos los datos modificados en la base de datos
    entrada_disponible.save()