from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView, CreateView
from .models import Evento

# Create your views here.
def index(request): 
    return render(request,'index.html')
def listar_eventos(request): 
    eventos = Evento.objects.all()  
    return render(request,'listar_eventos.html', {"eventos":eventos})

def ver_evento(request, evento_id): 
    evento = Evento.objects.get(id=evento_id)
    return render(request,'detalles_evento.html', {"evento":evento})
def borrar_evento(request, evento_id):
    Evento.objects.filter(pk=evento_id).delete()
    eventos = Evento.objects.all()
    return redirect('/eventos/')

class VistaEditarEvento(UpdateView):
    # specify the model you want to use
    model = Evento
    template_name="editar_evento.html"
    # specify the fields
    fields = [
        "fecha",
        "totalEntradas",
        "nombre",
        "descripcion",
        "ubicacion",
        "imagen",
    ]
    success_url ="/eventos/"

class VistaCrearEvento(CreateView):
    # specify the model you want to use
    model = Evento
    template_name="crear_evento.html"
    # specify the fields
    fields = [
        "fecha",
        "totalEntradas",
        "nombre",
        "descripcion",
        "ubicacion",
        "imagen",
        "empresa",
        "salt",
    ]
    success_url ="/eventos/"