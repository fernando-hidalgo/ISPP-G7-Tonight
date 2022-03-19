from django.shortcuts import render
import proyecto.qr

# Create your views here.
def index(request): 
    return render(request,'index.html')

def QR(request):
    proyecto.qr.read_qr_cam()
    return render(request,'qr.html')

def scan(request):
    return render(request, 'scan.html')
