from django.shortcuts import render
import proyecto.qr

# Create your views here.
def index(request): 
    return render(request,'index.html')

def QR(request):
    proyecto.qr.qr_init()
    return render(request,'qr.html')