import json
from django.http import HttpResponse
from django.shortcuts import render
import proyecto.qr
import proyecto.entrada
from proyecto.models import *

# Create your views here.
def index(request): 
    return render(request,'index.html')

def QR(request):
    proyecto.qr.read_qr_cam()
    return render(request,'qr.html')

def scan(request):
    if request.method == 'POST':
        data = request.POST.get('hash')
        evento = Evento.objects.get(id=1)
        proyecto.entrada.exchange_entrada(data, evento)
        return HttpResponse(status=200)
    else:
        return render(request, 'scan.html')

