import datetime
import qrcode
import qrcode.image.svg
import cv2
from proyecto.models import *
from proyecto.entrada import generate_hash
from io import BytesIO
import secrets

# Create your views here.
key_event = "FFFF"
path = 'static/img/'
#TICKET QRS
def generate_salt():
    return secrets.token_hex(16)

def render_qr(evento, entrada):
    data = ",".join([evento.nombre, entrada.hash])
    context = {}
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(data, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    context["svg"] = stream.getvalue().decode()
    return context

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
    img.save(path + entrada.hash + '.png')

def read_qr_cam():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        data, vertices_array, _ = detector.detectAndDecode(img)
        if vertices_array is not None:
            if data:
                cv2.imshow("img", img)
                if cv2.waitKey(1) == ord("q"):
                    cap.release()
                    cv2.destroyAllWindows()
                    print(data)
                    return data

def get_data(img):
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(img)
    if vertices_array is not None:
        print(data)
        return data
    else:
        print("There was some error")

def verify_qr(data, evento):
    if len(data.split(',')) == 2:
        name_event, qr_hash = data.split(',')
        entradas = Entrada.objects.all().filter(evento=evento.id)
        print("Entradas: ", entradas)
        for entrada in entradas:
            if entrada.hash == qr_hash:
                print("Okay")
                return entrada
    else:
        print("Invalid QR")
    return None


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

def init_qr():
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

