from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from tonight.proyecto.models import Cliente, Entrada, Evento

# asignamos una entrada disponible a un usuario
def conprarEntradas(request, nombre_evento):
    evento_ = Evento.objects.get(nombre=nombre_evento) # evento del que queremos entrada
    usuario = request.user # usuario que compra la entrada

    entradas = Entrada.objects.filter(evento=evento_).all()     
    entradas_vendidas = entradas.filter(estado='V').count()
    
    if evento_.totalEntradas > entradas_vendidas:
        entrada_disponible = entradas.filter(estado='E')
        #modificamos los valores de la entrada a vender
        entrada_disponible.fechaCompra=datetime.today
        entrada_disponible.cliente=usuario
        entrada_disponible.estado('V')
        # guardamos los datos modificados en la base de datos
        entrada_disponible.save()


    # asignamos una entrada disponible a un usuario
def venderEntradas(request, entrada_id):
    entrada = Entrada.objects.get(id=entrada_id)
    usuario = request.user
    if entrada.cliente == usuario:
        entrada.estado('E')
        entrada.save()
    
def cancelarVentaEntrada(request, entrada_id):
    entrada = Entrada.objects.get(id=entrada_id)
    usuario = request.user
    if entrada.cliente == usuario:
        entrada.estado('V')
        entrada.save()
