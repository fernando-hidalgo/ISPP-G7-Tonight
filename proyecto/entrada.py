import datetime
from django.shortcuts import render, get_object_or_404
from proyecto.models import *
import hashlib
import binascii
import hmac
import proyecto.qr

def generate_hash(key, msg):
    key = binascii.unhexlify(key)
    encoded = msg.encode()
    result = hmac.new(key, encoded, hashlib.sha256).hexdigest()
    return result

def create_entrada(cliente, evento):
    if cliente.saldo - evento.precioEntrada >= 0:
        cliente.saldo = cliente.saldo - evento.precioEntrada
        cliente.save()
        Entrada.objects.create(fechaCompra=datetime.date.today(), 
            fechaCaducidad=evento.fecha + datetime.timedelta(days=1), 
            estado='A',
            cliente=cliente,
            evento=evento,
            hash=generate_hash(evento.salt, ",".join([str(evento.id), str(cliente.user.id)]))
        )
    else:
        return False
    

def exchange_entrada(data, evento):
    """LLamamos a la la función de leer qr del qr.py y en caso de verificarse
    que dicha entrada es valida y esta activa, se pasa a estado vendida y devuelve un okay"""
    entrada = proyecto.qr.verify_qr(data, evento)
    if entrada is not None:
        if entrada.estado == 'A':
            entrada.estado = 'U'
            entrada.save()
            print("Entrada leida")
            return True
        else:
            print("Esta entrada no está en estado Adquirida")
            return False
    else:
        print("No se ha encontrado una entrada")
        return False

