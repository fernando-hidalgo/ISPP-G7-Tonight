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
    entrada = Entrada.objects.create(fechaCompra=datetime.date.today(), 
        fechaCaducidad=evento.fecha + datetime.timedelta(days=1), 
        estado=1,
        cliente=cliente,
        evento=evento,
        hash=generate_hash(evento.salt, ",".join([str(evento.id), str(cliente.user.id)]))
    )
    return entrada

def exchange_entrada(data, evento):
    """LLamamos a la la función de leer qr del qr.py y en caso de verificarse
    que dicha entrada es valida y esta activa, se pasa a estado vendida y devuelve un okay"""
    entrada = proyecto.qr.verify_qr(data, evento)
    if entrada is not None:
        if entrada.estado == 1:
            entrada.estado = 3
            print("Entrada leida")
            return True
    print("No se ha encontrado una entrada")
    return False
