from hashlib import new
from time import time
from urllib import request
from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model
from proyecto.models import Cliente, Empresa, Evento, Entrada, Transaccion
from django.contrib.auth.models import User
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView, CreateView

from .models import Evento
import proyecto.qr
import proyecto.entrada
import proyecto.transacciones
import datetime
from proyecto.forms import TransactionForm
from proyecto.transacciones import poner_venta,poner_compra
from proyecto.entrada import create_entrada

User = get_user_model()

# Create your views here.
def listar_eventos(request): 
    eventos = Evento.objects.all()
    return render(request,'listar_eventos.html', {"eventos":eventos})

def QR(request):
    proyecto.qr.init_qr()
    return render(request,'qr.html')

def scan(request):
    if request.method == 'POST':
        print("funciona")
        data = request.POST.get('hash')
        evento = Evento.objects.get(id=4)
        proyecto.entrada.exchange_entrada(data, evento)
        return HttpResponse(status=200)
    else:
        return render(request, 'scan.html')

class InicioVista(View):
    def get(self, request):
        if request.user.id == None:
            response = redirect('/error/')
            return response
        hayUsuario = User.objects.filter(id=request.user.id).exists()
        if hayUsuario == True:
            usuario = User.objects.get(id=request.user.id)
            empresa_exists = (Empresa.objects.filter(user = usuario).count() > 0)
            cliente_exists = (Cliente.objects.filter(user = usuario).count() > 0)
            if empresa_exists:
                response = redirect('/welcome_bussiness/')
                return response
            if cliente_exists:
                response = redirect('/welcome_client/')
                return response
        else:
            response = redirect('/error/')
            return response

class ErrorVista(TemplateView):
    template_name = 'error.html'

class WelcomeClient(View):
    def get(self, request):
        if request.user.id == None:
            response = redirect('/error/')
            return response
        hayUsuario = User.objects.filter(id=request.user.id).exists()
        if hayUsuario == True:
            usuario = User.objects.get(id=request.user.id)
            cliente_exists = (Cliente.objects.filter(user = usuario).count() > 0)
            if not cliente_exists:
                response = redirect('/error/')
                return response
            else:
                cliente = Cliente.objects.get(user=usuario)
                context = {
                    'cliente': cliente
                }
                return render (request, 'welcome_client.html')
        else:
            response = redirect('/error/')
            return response

class ClientProfile(View):
    def get(self, request, id):
        if request.user.id == None:
            response = redirect('/error/')
            return response
        hayUsuario = User.objects.filter(id=id).exists()
        if hayUsuario == True:
            usuario = User.objects.get(id=id)
            cliente_exists = (Cliente.objects.filter(user = usuario).count() > 0)
            if str(request.user.id) != str(id) or not cliente_exists:
                response = redirect('/error/')
                return response
            else:
                cliente = Cliente.objects.get(user=usuario)
                hayEntradas = Entrada.objects.filter(cliente=cliente).exists()
                if hayEntradas == True:
                    entradas = Entrada.objects.filter(cliente=cliente)
                    context = {
                        'cliente': cliente,
                        'entradas': entradas
                    }
                else:
                    context = {
                        'cliente': cliente
                    }
                return render (request, 'cliente.html', context)
        else:
            response = redirect('/error/')
            return response
        
class WelcomeBusiness(View):
    def get(self, request):
        if request.user.id == None:
            response = redirect('/error/')
            return response
        hayUsuario = User.objects.filter(id=request.user.id).exists()
        if hayUsuario == True:
            usuario = User.objects.get(id=request.user.id)
            empresa_exists = (Empresa.objects.filter(user = usuario).count() > 0)
            if not empresa_exists:
                response = redirect('/error/')
                return response
            else:
                return render (request, 'welcome_bussiness.html')
        else:
            response = redirect('/error/')
            return response

class BusinnessProfile(View):
    def get(self, request, id):
        if request.user.id == None:
            response = redirect('/error/')
            return response
        hayUsuario = User.objects.filter(id=id).exists()
        if hayUsuario == True:
            usuario = User.objects.get(id=id)
            empresa_exists = (Empresa.objects.filter(user = usuario).count() > 0)
            if str(request.user.id) != str(id) or not empresa_exists:
                response = redirect('/error/')
                return response
            else:
                empresa = Empresa.objects.get(user=usuario)
                hayEventos = Evento.objects.filter(empresa=empresa).exists()
                if hayEventos == True:
                    eventos = Evento.objects.filter(empresa=empresa)
                    context = {
                        'empresa': empresa,
                        'eventos': eventos
                    }
                else:
                    context = {
                        'empresa': empresa,
                    }
                return render (request, 'empresa.html', context)
        else:
            response = redirect('/error/')
            return response

def ver_evento(request, evento_id): 
    no_log = True
    no_duenho = False
    es_duenho = False
    entrada = None
    transaccion = None
    hay_evento = Evento.objects.filter(id=evento_id).exists()
    print(request.user)
    if hay_evento == True:
        if request.user.id==None:
            response = redirect('/error/')
            return response
        else:
            usuario = User.objects.get(id=request.user.id)
            empresa_exists = (Empresa.objects.filter(user = usuario).count() > 0)
            cliente_exists = (Cliente.objects.filter(user = usuario).count() > 0)
            evento = Evento.objects.get(id=evento_id)
            if cliente_exists:
                cliente = Cliente.objects.get(user = usuario)
                no_duenho = True
                entrada_exists = Entrada.objects.filter(cliente = cliente, evento = evento)
                transaccion_exists = Transaccion.objects.filter(cliente = cliente, evento = evento, tipo = 'V', done = False)
                if entrada_exists.count() > 0:
                    entrada = entrada_exists.first()
                if transaccion_exists.count() > 0:
                    transaccion = transaccion_exists.first()
            elif empresa_exists:
                es_duenho = evento.empresa==Empresa.objects.get(user = usuario)
            return render(request,'detalles_evento.html', {"evento":evento,"no_log":no_log,"no_duenho":no_duenho,
                    "es_duenho":es_duenho,"user":usuario, "has_entrada": entrada is not None,
                     "en_venta": transaccion is not None})
    else:
        response = redirect('/error/')
        return response

def borrar_evento(request, evento_id):
    if request.user.id == None:
            response = redirect('/error/')
            return response
    hay_evento = Evento.objects.filter(id=evento_id).exists()
    if hay_evento == True:
        Evento.objects.filter(pk=evento_id).delete()
        eventos = Evento.objects.all()
        return redirect('/empresa/'+str(request.user.id)+'/')
    else:
        response = redirect('/error/')
        return response

class VistaEditarEvento(UpdateView):
    # specify the model you want to use
    model = Evento
    template_name="editar_evento.html"
    # specify the fields
    fields = [
        "fecha",
        "precioEntrada",
        "totalEntradas",
        "nombre",
        "descripcion",
        "ubicacion",
        "imagen",
    ]
    success_url ="/welcome_bussiness/"

class VistaCrearEvento(CreateView):
    # specify the model you want to use
    model = Evento
    success_url ="/welcome_bussiness/"
    template_name="crear_evento.html"
    # specify the fields
    fields = [
        "fecha",
        "precioEntrada",
        "totalEntradas",
        "nombre",
        "descripcion",
        "ubicacion",
        "imagen",
        "salt",
    ]
    def form_valid(self, form):
        form.instance.empresa = Empresa.objects.get(user =self.request.user)
        return super().form_valid(form)


class Entradas(View):
    def get(self, request, id):
        print('El id es'+id)
        entrada = Entrada.objects.get(id=id)
        if request.method == 'POST':
            id = request.POST.get('id')
        print(entrada)
        return render(request,'detalles_evento.html', {"entrada":entrada})

def vender(request, evento_id):
    if request.method == 'POST':
        form = proyecto.forms.TransactionForm(request.POST)
        evento = Evento.objects.get(id=evento_id)
        if form.is_valid():
            usuario = User.objects.get(id=request.user.id)
            dia = form.cleaned_data["dia"]
            hora = form.cleaned_data["hora"]
            fechLimite = datetime.datetime.combine(dia,hora)
            cliente = Cliente.objects.get(user = usuario)
            poner_venta(evento, cliente, fechLimite)
        return redirect(ver_evento, evento_id=evento.id)
    else:
        form = proyecto.forms.TransactionForm()
        return render(request, 'transaccion.html', {'form':form, 'id':evento_id})

def orden_comprar(request, evento_id):
    if request.method == 'POST':
        form = proyecto.forms.TransactionForm(request.POST)
        evento = Evento.objects.get(id=evento_id)
        if form.is_valid():
            usuario = User.objects.get(id=request.user.id)
            dia = form.cleaned_data["dia"]
            hora = form.cleaned_data["hora"]
            fechLimite = datetime.datetime.combine(dia,hora)
            cliente = Cliente.objects.get(user = usuario)
            poner_compra(evento, cliente, fechLimite)
        return redirect(ver_evento, evento_id=evento.id)
    else:
        form = proyecto.forms.TransactionForm()
        return render(request, 'transaccion.html', {'form':form, 'id':evento_id})
    
def cancelar_transaccion(request, evento_id):
    o_user = User.objects.get(id=request.user.id)
    evento = Evento.objects.get(id=evento_id)
    cliente = Cliente.objects.get(user = o_user)
    transaccion = Transaccion.objects.filter(cliente = cliente, evento = evento, tipo = 'V', done = False).first()
    proyecto.transacciones.cancelar_transaccion(transaccion)
    return redirect(ver_evento, evento_id=evento.id)

def compra_directa(request, evento_id):
    o_user = User.objects.get(id=request.user.id)
    cliente = Cliente.objects.get(user = o_user)
    evento = Evento.objects.get(id=evento_id)
    create_entrada(cliente,evento)
    return redirect(ver_evento, evento_id=evento.id)