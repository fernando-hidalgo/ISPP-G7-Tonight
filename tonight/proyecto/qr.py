import datetime
from django.shortcuts import render, get_object_or_404
import qrcode
import hashlib
import binascii
import hmac
import cv2
from proyecto.models import *
# Create your views here.
key_event = "FFFF"
path = 'static/img/qrcode001.png'
#TICKET QRS
def generate_hash(key, msg):
    key = binascii.unhexlify(key)
    encoded = msg.encode()
    result = hmac.new(key, encoded, hashlib.sha256).hexdigest()
    return result
    
def generate_qr(cliente, entrada, evento):
    """Datos a meter en el qr: 
    - Usuario (nombre)
    - Evento (nombre)
    - Hash(Evento (id) + Usuario(id))

    ¿Qué es lo que quiere comprobar el local?
    - Que la entrada es para ese evento
    - Que la entrada pertenece a esa persona
    """
    
    input_data = ",".join([evento.nombre, entrada.hash])

    qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(path)

def get_data():
    filename = path
    image = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
    if vertices_array is not None:
        print(data)
        return data
    else:
        print("There was some error")

def verify_qr(data, evento):
    if len(data.split(',')) == 2:
        name_event, qr_hash = data.split(',')
        entradas = [entrada.hash for entrada in Entrada.objects.all().filter(evento=evento.id)]
        print("Entradas: ", entradas)
        if qr_hash in entradas:
            print(name_event, qr_hash)
            print("Okay")
    else:
        print("Invalid QR")

def create_events_test():
    user = User.objects.create(username="u_piloto1", password="pass_prueba1")
    empresa = Empresa.objects.create(user=user, tlf=656565656)
    evento = Evento.objects.create(fecha=datetime.date.today(), totalEntradas=40, nombre="evento 1", ubicacion="Sevilla", empresa=empresa)
    cliente = Cliente.objects.create(saldo=293, tlf=655656565, user=user)
    entrada = Entrada.objects.create(fechaCompra=datetime.date.today(), 
        fechaCaducidad=datetime.date.today(), 
        estado=1,
        cliente=cliente,
        evento=evento,
        hash=generate_hash(key_event, ",".join([str(evento.id), str(cliente.user.id)]))
        )
    print(empresa)
    print(evento)
    print(cliente)
    print(entrada)
    return cliente, evento, entrada

def qr_init():
    User.objects.all().delete()
    Evento.objects.all().delete()
    Empresa.objects.all().delete()
    Cliente.objects.all().delete()
    Entrada.objects.all().delete()
    cliente, evento, entrada = create_events_test()
    print(Evento.objects.all())
    print(Empresa.objects.all())
    print(Cliente.objects.all())
    for e in Entrada.objects.all():
        print(e.hash)

    generate_qr(cliente, entrada, evento)
    data = get_data()
    verify_qr(data, evento)