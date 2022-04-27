import datetime
from django.shortcuts import render, get_object_or_404
from proyecto.models import *
import hashlib
import binascii
import hmac
import proyecto.qr
from django.contrib import messages

def generate_hash(key, msg):
    key = binascii.unhexlify(key)
    encoded = msg.encode()
    result = hmac.new(key, encoded, hashlib.sha256).hexdigest()
    return result

def create_entrada(request, cliente, evento):
    if evento.totalEntradas > 0:
        if cliente.saldo - evento.precioEntrada >= 0:
            cliente.saldo = cliente.saldo - evento.precioEntrada
            evento.totalEntradas -= 1
            evento.save()
            cliente.save()
            proyecto.notificaciones.send_notificacion(cliente.user.id, "Se ha comprado una entrada para " + evento.nombre)
            Entrada.objects.create(fechaCompra=datetime.date.today(), 
                fechaCaducidad=evento.fecha + datetime.timedelta(days=1), 
                estado='A',
                cliente=cliente,
                evento=evento,
                hash=generate_hash(evento.salt, ",".join([str(evento.id), str(cliente.user.id)]))
            )
            return True
        else:
            messages.info(request, 'No tienes saldo!')
            return False
    else:
        print("No hay entradas disponibles")
        messages.info(request, 'No hay entradas disponibles')
        return False
    

def exchange_entrada(request, data, evento):
    """LLamamos a la la función de leer qr del qr.py y en caso de verificarse
    que dicha entrada es valida y esta activa, se pasa a estado vendida y devuelve un okay"""
    print(data)
    print(evento)
    entrada = proyecto.qr.verify_qr(data, evento)
    print(entrada)
    if entrada is not None:
        if entrada.estado == 'A':
            entrada.estado = 'U'
            entrada.save()
            msg = 'La entrada es correcta'
        elif entrada.estado == 'C':
            msg = 'La entrada está caducada'
        elif entrada.estado == 'U':
            msg = 'Esta entrada ya ha sido escaneada'
        else:
            msg = 'Esta entrada no puede ser escaneada (¿está en venta?)'
        return msg
    else:
        msg = 'No se ha encontrado una entrada'
        return msg

def check_dates(cliente):
    entradas = Entrada.objects.filter(cliente = cliente)
    for entrada in entradas:
        if datetime.datetime.now() > entrada.fechaCaducidad:
            entrada.estado = 'C'
            entrada.save()