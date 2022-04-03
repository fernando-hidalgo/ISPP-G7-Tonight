from urllib import request
from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model, authenticate, login
from proyecto.models import Cliente, Empresa, Evento, Entrada, Transaccion, Empleado
from django.contrib.auth.models import User
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView, CreateView
from .forms import UserForm, ClienteModelForm, EmpresaModelForm
from .models import Evento
from django.utils import timezone
import proyecto.qr
import proyecto.entrada
from proyecto.forms import PaypalAmountForm
from hashlib import new
from time import time
from datetime import date, datetime
import proyecto.transacciones
import datetime
from proyecto.forms import TransactionForm
from proyecto.transacciones import poner_venta,poner_compra
from proyecto.entrada import create_entrada
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

User = get_user_model()
rec = 0

# Create your views here.
def listar_eventos(request): 
    eventos = Evento.objects.all()
    return render(request,'listar_eventos.html', {"eventos":eventos})

def QR(request, evento_id):
    if request.user.id == None:
        return redirect('/error/')
    evento = get_object_or_404(Evento, id = evento_id)
    user = User.objects.get(id = request.user.id)
    cliente = Cliente.objects.get(user = user)
    entrada_exists = Entrada.objects.filter(cliente = cliente, evento = evento)
    if entrada_exists.count() > 0:
        entrada = entrada_exists.first()
        context = proyecto.qr.render_qr(evento, entrada)
        return render(request, "qr.html", context=context)
    else:
        return redirect('/error/')

def scan(request, evento_id):
    evento = get_object_or_404(Evento, id = evento_id)
    if request.method == 'POST':
        print("funciona")
        data = request.POST.get('hash')
        proyecto.entrada.exchange_entrada(data, evento)
        return HttpResponse(status=200)
    else:
        return render(request, 'scan.html')
def listar_eventos_empleado(request, empleado_id): 
    hayUsuario = User.objects.filter(id=request.user.id).exists()
    if hayUsuario == True:
        usuario = User.objects.get(id=request.user.id)
        empleado_exists = (Empleado.objects.filter(user = usuario).count() > 0)
        if empleado_exists:
            empleado = Empleado.objects.get(user = usuario)
            eventos = Evento.objects.filter(empresa = empleado.empresa, fecha__range=[str(timezone.now()), "7777-07-07"])
            return render(request,'empleado.html', {"eventos":eventos})
        else:
            response = redirect('/error/')
            return response
    else:
        response = redirect('/error/')
        return response

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
                response = redirect('/empresa/{}/'.format(request.user.id))
                return response
            if cliente_exists:
                response = redirect('/eventos/')
                return response
            else:
                response = redirect('/admin/')
                return response
        else:
            response = redirect('/error/')
            return response

class ErrorVista(TemplateView):
    template_name = 'error.html'

class WelcomeVista(TemplateView):
    template_name = 'welcome.html'

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

class ClientCreate(CreateView):
     # specify the model you want to use
    model = Cliente
    template_name="crear_cliente.html"
    # specify the fields
    form_class = UserForm
    second_form_class = ClienteModelForm
    success_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super(ClientCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            cliente = form2.save(commit=False)
            cliente.saldo = 0
            cliente.user = form.save()
            cliente.save()
            return redirect('/login/')
        else:
            return render (request, 'crear_cliente.html', {'form': form, 'form2': form2})

    def form_valid(self, form, form2):
        form.save()
        form2.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        usuario = authenticate(username=usuario, password=password)
        return redirect('/login/')

class EmpleadoCreate(CreateView):
     # specify the model you want to use
    model = Empleado
    template_name="crear_empleado.html"
    # specify the fields
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super(EmpleadoCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            empleado = Empleado()
            empleado.user = form.save()
            empleado.empresa = Empresa.objects.get(user = request.user)
            print(request.user.id)
            empleado.save()
            return redirect('/empresa/' + str(request.user.id) + '/')
        else:
            return redirect('/error/')

    def form_valid(self, form):
        form.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        usuario = authenticate(username=usuario, password=password)
        return redirect('/login/')

class EmpresaCreate(CreateView):
     # specify the model you want to use
    model = Empresa
    template_name="crear_empresa.html"
    # specify the fields
    form_class = UserForm
    second_form_class = EmpresaModelForm
    success_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super(EmpresaCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            empresa = form2.save(commit=False)
            usuario = form.save()
            empresa.user = usuario
            empresa.save()
            empleado = Empleado()
            empleado.empresa = empresa
            usuario2 = User()
            usuario2.username = 'empleado_'+empresa.user.username
            usuario2.password = empresa.user.password
            usuario2.email = empresa.user.email
            usuario2.save()
            empleado.user = usuario2
            empleado.save()
            return redirect('/login/')
        else:
            return render (request, 'crear_empresa.html', {'form': form, 'form2': form2})

    def form_valid(self, form, form2):
        form.save()
        form2.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        usuario = authenticate(username=usuario, password=password)
        return redirect('/login/')

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
                transaccion_exists = Transaccion.objects.filter(cliente = cliente, evento = evento, done = False).exclude(tipo = 'N')
                if entrada_exists.count() > 0:
                    entrada = entrada_exists.first()
                if transaccion_exists.count() > 0:
                    transaccion = transaccion_exists.first()
            elif empresa_exists:
                es_duenho = evento.empresa==Empresa.objects.get(user = usuario)
            return render(request,'detalles_evento.html', {"evento":evento,"no_log":no_log,"no_duenho":no_duenho,
                    "es_duenho":es_duenho,"user":usuario, "has_entrada": entrada is not None,
                     "hay_transaccion": transaccion is not None})
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
    ]
    def form_valid(self, form):
        form.instance.empresa = Empresa.objects.get(user =self.request.user)
        form.instance.salt = proyecto.qr.generate_salt()
        return super().form_valid(form)

    def get_success_url(self):
        return "/empresa/" + str(self.request.user.id) + "/"

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
            if fechLimite < datetime.datetime.now() or fechLimite > evento.fecha:
                messages.add_message(request,messages.WARNING,message="La fecha debe ser superior a hoy y menor que el evento")
                return redirect("/eventos/"+str(evento.id)+"/vender")
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
            if fechLimite < datetime.datetime.now() or fechLimite > evento.fecha:
                messages.add_message(request,messages.WARNING,message="La fecha debe ser superior a hoy y menor que el evento")
                return redirect("/eventos/"+str(evento.id)+"/orden_comprar")
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
    transaccion = Transaccion.objects.filter(cliente = cliente, evento = evento, done = False).exclude(tipo = 'N').first()
    proyecto.transacciones.cancelar_transaccion(transaccion)
    return redirect(ver_evento, evento_id=evento.id)

def compra_directa(request, evento_id):
    o_user = User.objects.get(id=request.user.id)
    cliente = Cliente.objects.get(user = o_user)
    evento = Evento.objects.get(id=evento_id)
    create_entrada(cliente,evento)
    return redirect(ver_evento, evento_id=evento.id)
def recargar_saldo(request, id):
    if request.method == 'POST':
        form = proyecto.forms.PaypalAmountForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data["cantidad"]
            
            host = request.get_host()
            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': cantidad,
                'item_name': 'Recarga Saldo Tonight',
                'currency_code': 'EUR',
                'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
                'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
            }
            
            global rec
            rec = cantidad

            form = PayPalPaymentsForm(initial=paypal_dict)
            return render(request, 'saldo_procesar_pago.html', {'form': form})
    else:
        form = proyecto.forms.PaypalAmountForm()
        return render(request, 'saldo_opciones.html', {'form':form})
        
@csrf_exempt
def payment_done(request):
    global rec
    o_user = User.objects.get(id=request.user.id)
    cliente = Cliente.objects.get(user = o_user)
    
    cliente.saldo += rec
    cliente.save()
    return render(request, 'saldo_exito.html', {'cantidad': rec, 'total': cliente.saldo})

@csrf_exempt
def payment_canceled(request):
    return render(request, 'saldo_cancelado.html')