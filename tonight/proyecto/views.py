from urllib import request
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
from .forms import UserForm, ClienteModelForm, EmpresaModelForm
from .models import Evento
import proyecto.qr
import proyecto.entrada

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
                response = redirect('/empresa/'+str(request.user.id)+'/')
                return response
            if cliente_exists:
                response = redirect('/eventos/')
                return response
        else:
            response = redirect('/error/')
            return response

class ErrorVista(TemplateView):
    template_name = 'error.html'

class WelcomeVista(TemplateView):
    template_name = 'welcome.html'

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
            return redirect('/error/')

    def form_valid(self, form, form2):
        form.save()
        form2.save()
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
            empresa.user = form.save()
            empresa.save()
            return redirect('/login/')
        else:
            return redirect('/error/')

    def form_valid(self, form, form2):
        form.save()
        form2.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        usuario = authenticate(username=usuario, password=password)
        return redirect('/login/')

        
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
            if cliente_exists:
                no_duenho = True
                evento = Evento.objects.get(id=evento_id)
                return render(request,'detalles_evento.html', {"evento":evento,"no_log":no_log,"no_duenho":no_duenho,"es_duenho":es_duenho,"user":usuario})
            elif empresa_exists:
                evento = Evento.objects.get(id=evento_id)
                es_duenho = evento.empresa==Empresa.objects.get(user = usuario)
                return render(request,'detalles_evento.html', {"evento":evento,"no_log":no_log,"no_duenho":no_duenho,"es_duenho":es_duenho,"user":usuario})
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
        print(id)
        entrada = Entrada.objects.get(id=id)
        if request.method == 'POST':
            id = request.POST.get('id')
        print(entrada)
        return render(request,'entrada.html', {"entrada":entrada})

    #def vender(self, request, id):
        #o_user = User.objects.get(id=request.user.id)
        #cliente = Cliente.objects.get(user = o_user)
        #proyecto.transacciones.poner_venta(evento, cliente, fech)