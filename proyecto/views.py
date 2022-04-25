from re import template
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
from .forms import UserForm, ClienteModelForm, EmpresaModelForm, FiestaForm, FiestaEditForm, EmpresaEditForm, UserEditForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Evento, Notificacion
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
import proyecto.notificaciones
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from geopy.geocoders import Nominatim
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import json

User = get_user_model()
rec = 0

@login_required
def listar_eventos(request):
    #Solo los Clientes tienen acceso
    acceso = Cliente.objects.filter(user = request.user.id)
    if(acceso):
        #Se obtienen todos los eventos. Se itera cada uno de ellos, para comprobar cuales pasan a estar en estado Acabado
        eventos = Evento.objects.all()
        for x in eventos:
            #Si la fecha actual es mayor que la fecha de incio mas x horas, se considera que el Evento ha acabado
            if(timezone.now() > x.fecha + timezone.timedelta(hours=3)):
                x.estado = 'A'
                x.save()     
        #Luego se hace un GET de aquellos con estado En Curso
        eventos = Evento.objects.filter(estado = 'E')
        return render(request,'listar_eventos.html', {"eventos":eventos})
    else:
        return redirect('/')

@login_required
def listar_eventos_empleado(request, id):
    #Solo los Empleados tienen acceso
    acceso = Empleado.objects.filter(user = request.user.id)
    if(acceso):
        #Se obtienen todos los eventos. Se itera cada uno de ellos, para comprobar cuales pasan a estar en estado Acabado
        eventos = Evento.objects.all()
        for x in eventos:
            #Si la fecha actual es mayor que la fecha de incio mas x horas, se considera que el Evento ha acabado
            if(timezone.now() > x.fecha + timezone.timedelta(hours=3)):
                x.estado = 'A'
                x.save()     
        #Luego se hace un GET de aquellos con estado En Curso
        eventos = Evento.objects.filter(estado = 'E')
        return render(request,'empleado.html', {"eventos":eventos})
    else:
        return redirect('/')

@login_required
def mapa_eventos(request): 
    #Solo los Clientes tienen acceso
    acceso = Cliente.objects.filter(user = request.user.id)
    if(acceso):
        eventos = Evento.objects.all()
        for x in eventos:
            #Si la fecha actual es mayor que la fecha de incio mas x horas, se considera que el Evento ha acabado
            if(timezone.now() > x.fecha + timezone.timedelta(hours=3)):
                x.estado = 'A'
                x.save()     
        #Luego se hace un GET de aquellos con estado En Curso
        eventos = Evento.objects.filter(estado = 'E')
        map_list = []
        for x in eventos:
            map_list.append(x.latitud)
            map_list.append(x.longitud)
            map_list.append(x.id)
        return render(request,'mapa_eventos.html', {"fiestas":map_list})
    else:
        return redirect('/')

@login_required
def QR(request, evento_id):
    #Solo los Clientes tienen acceso
    acceso = Cliente.objects.filter(user = request.user.id)
    if(acceso):
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
    else:
        return redirect('/')

@login_required
def scan(request, evento_id):
    #Solo los Empleados tienen acceso
    acceso = Empleado.objects.filter(user = request.user.id)
    if(acceso):
        evento = get_object_or_404(Evento, id = evento_id)
        if request.method == 'POST':
            print("funciona")
            data = request.POST.get('hash')
            msg = proyecto.entrada.exchange_entrada(request, data, evento)
            messages.add_message(request,messages.INFO,message=msg)

            django_messages = []
            for message in messages.get_messages(request):
                django_messages.append(message.message)

            data_ajax = {}
            data_ajax['messages'] = django_messages

            print(msg)
            return HttpResponse(json.dumps(data_ajax), content_type="application/json")
        else:
            return render(request, 'scan.html')
    else:
        return redirect('/')

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
            empleado_exists = (Empleado.objects.filter(user = usuario).count() > 0)
            if empresa_exists:
                response = redirect('/empresa/{}/'.format(request.user.id))
                return response
            if cliente_exists:
                response = redirect('/eventos/')
                return response
            if empleado_exists:
                response = redirect('/empleados/{}/'.format(request.user.id))
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

class TerminosVista(TemplateView):
    template_name = 'terminos.html'

class ClientProfile(LoginRequiredMixin, View):
    def get(self, request, id):
        #Solo los Clientes tienen acceso a su propio perfil
        acceso = Cliente.objects.filter(user = request.user.id)
        if(acceso):
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
                    notificaciones = proyecto.notificaciones.count_unread_notificaciones(request.user.id)
                    if hayEntradas == True:
                        entradas = Entrada.objects.filter(cliente=cliente)
                        context = {
                            'cliente': cliente,
                            'entradas': entradas,
                            'notificaciones': notificaciones
                        }
                    else:
                        context = {
                            'cliente': cliente,
                            'notificaciones': notificaciones
                        }
                    return render (request, 'cliente.html', context)
            else:
                response = redirect('/error/')
                return response
        else:
            return redirect('/')

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


class ClientEdit(UpdateView):
    # specify the model you want to use
    model = User
    second_model=Cliente
    template_name="editar_cliente.html"
    # specify the fields
    form_class = UserEditForm
    second_form_class = ClienteModelForm

    def get_context_data(self, **kwargs):
        context = super(ClientEdit, self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk')
        cliente=self.second_model.objects.get(id=pk)
        user=self.model.objects.get(id=cliente.user.id)
        context['form'] = self.form_class(instance=user)
        context['form2'] = self.second_form_class(instance=cliente)
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        id_cliente=kwargs['pk']
        cliente=self.second_model.objects.get(id=id_cliente)
        user=self.model.objects.get(id=cliente.user.id)
        form = self.form_class(request.POST, instance=user)
        form2 = self.second_form_class(request.POST, request.FILES, instance=cliente)
        if form.is_valid() and form2.is_valid():
            cliente = form2.save(commit=False)
            cliente.user = form.save()
            cliente.save()
            return redirect('/cliente/{}/'.format(self.request.user.id))
        else:
            return render (request, 'editar_cliente.html', {'form': form, 'form2': form2})

    # def form_valid(self, form):
    #     context=self.get_context_data()
    #     user=context["user"]
    #     self.object = form.save()
    #     if user.is_valid():
    #         user.instance=self.object
    #         user.save()
    #         response = redirect('/cliente/{}/'.format(self.request.user.id))
    #     else:
    #         response=redirect('/error')
        
    #     return response

def cambiar_contra(request, pk):
    hay_cliente=Cliente.objects.filter(user_id=pk).exists()
    hay_empresa=Empresa.objects.filter(user_id=pk).exists()
    user=User.objects.get(id=pk)
    if(request.user!=user):
        return redirect('/error/')
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        if hay_cliente:
            cliente = Cliente.objects.get(user=user)
            user2=form.save()
            update_session_auth_hash(request,user2) 
            return redirect('/cliente/{}/'.format(cliente.user.id))
        if hay_empresa:
            empresa= Empresa.objects.get(user=user)
            user2=form.save()
            update_session_auth_hash(request,user2) 
            return redirect('/empresa/{}/'.format(empresa.user.id))
    else:
        return render (request, 'editar_contra.html', {'form': form})


@login_required
def borrar_cliente(request, id):
    #Solo ese usuario tiene acceso
    acceso = Cliente.objects.filter(user = request.user.id)
    if(acceso):
        if request.user.id == None:
                response = redirect('/error/')
                return response
        hay_cliente = Cliente.objects.filter(user_id=id).exists()
        if hay_cliente == True and str(request.user.id) == str(id):
            Cliente.objects.filter(user_id=id).delete()
            User.objects.filter(id=id).delete()
            return redirect('/')
        else:
            response = redirect('/error/')
            return response
    else:
        return redirect('/')

class EmpleadoCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # specify the model you want to use
    model = Empleado
    template_name="crear_empleado.html"
    # specify the fields
    form_class = UserForm
    
    def test_func(self):
        return Empresa.objects.filter(user = self.request.user.id)

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
            return render (request, 'crear_empleado.html', {'form': form})

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
            usuario2.email = 'empleado_'+empresa.user.email
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

class EmpresaEdit(UpdateView):
    # specify the model you want to use
    model = User
    second_model= Empresa
    template_name="editar_empresa.html"
    # specify the fields
    form_class = UserEditForm
    second_form_class = EmpresaEditForm

    def get_context_data(self, **kwargs):
        context = super(EmpresaEdit, self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk')
        empresa=self.second_model.objects.get(id=pk)
        user=self.model.objects.get(id=empresa.user.id)
        if(user.id!= self.request.user.id):
            return redirect('/error/')
        else:
            context['form'] = self.form_class(instance=user)
            context['form2'] = self.second_form_class(instance=empresa)
            return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        id_empresa=kwargs['pk']
        empresa=self.second_model.objects.get(id=id_empresa)
        user=self.model.objects.get(id=empresa.user.id)
        form = self.form_class(request.POST, instance=user)
        form2 = self.second_form_class(request.POST, request.FILES, instance=empresa)
        if form.is_valid() and form2.is_valid():
            cliente = form2.save(commit=False)
            cliente.user = form.save()
            cliente.save()
            return redirect('/empresa/{}/'.format(self.request.user.id))
        else:
            return render (request, 'editar_empresa.html', {'form': form, 'form2': form2})

class BusinnessProfile(LoginRequiredMixin, View):
    def get(self, request, id):
        #Solo las Empresas tienen acceso a su propio perfil
        acceso = Empresa.objects.filter(user = request.user.id)
        if(acceso):
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
        else:
            return redirect('/')

@login_required
def borrar_empresa(request, id):
    #Solo ese usuario tiene acceso
    acceso = Empresa.objects.filter(user = request.user.id)
    if(acceso):
        if request.user.id == None:
                response = redirect('/error/')
                return response
        hay_empresa = Empresa.objects.filter(user_id=id).exists()
        if hay_empresa == True and str(request.user.id) == str(id):
            Empresa.objects.filter(user_id=id).delete()
            User.objects.filter(id=id).delete()
            return redirect('/')
        else:
            response = redirect('/error/')
            return response
    else:
        return redirect('/')

@login_required
def ver_evento(request, evento_id): 
    no_log = True
    no_duenho = False
    es_duenho = False
    es_empleado = False
    entrada = None
    transaccion = None
    entrada_used_cad = False
    hay_evento = Evento.objects.filter(id=evento_id).exists()
    if hay_evento == True:
        if request.user.id==None:
            response = redirect('/error/')
            return response
        else:
            usuario = User.objects.get(id=request.user.id)
            empresa_exists = (Empresa.objects.filter(user = usuario).count() > 0)
            cliente_exists = (Cliente.objects.filter(user = usuario).count() > 0)
            empleado_exists = (Empleado.objects.filter(user = usuario).count() > 0)
            evento = Evento.objects.get(id=evento_id)
            if (evento.fecha + timezone.timedelta(hours=3) < timezone.now()) or evento.estado == 'A':
                evento.estado = 'A'
                evento.save()
                return redirect('/error/')
            if empleado_exists:
                empleado = Empleado.objects.get(user = usuario)
                if empleado.empresa ==  evento.empresa:
                    es_empleado = True
            if cliente_exists:
                cliente = Cliente.objects.get(user = usuario)
                no_duenho = True
                entrada_exists = Entrada.objects.filter(cliente = cliente, evento = evento).exclude(estado='V')
                transaccion_exists = Transaccion.objects.filter(cliente = cliente, evento = evento, done = False).exclude(tipo = 'N')
                
                if entrada_exists.count() > 0:
                    entrada = entrada_exists.first()
                    if entrada.estado == 'U' or entrada.estado == 'C':
                        entrada_used_cad = True
                if transaccion_exists.count() > 0:
                    transaccion = transaccion_exists.first()
                    print(transaccion)
                    print(transaccion is not None)
                    print(entrada is not None)
            elif empresa_exists:
                es_duenho = evento.empresa==Empresa.objects.get(user = usuario)
            return render(request,'detalles_evento.html', {"evento":evento,"no_log":no_log,"no_duenho":no_duenho,
                    "es_duenho":es_duenho,"es_empleado":es_empleado,"user":usuario, "has_entrada": entrada is not None,
                     "hay_transaccion": transaccion is not None, "entrada_used_cad": entrada_used_cad})
    else:
        response = redirect('/error/')
        return response

@login_required
def borrar_evento(request, evento_id):
    #Solo las Empresas tienen acceso
    acceso = Empresa.objects.filter(user = request.user.id)
    if(acceso):
        if request.user.id == None:
                response = redirect('/error/')
                return response
        hay_evento = Evento.objects.filter(id=evento_id).exists()
        if hay_evento == True:
            Evento.objects.filter(pk=evento_id).delete()
            eventos = Evento.objects.all()
            proyecto.notificaciones.send_notificacion(request.user.id, "Se ha borrado el evento de manera satisfactoria")
            return redirect('/empresa/'+str(request.user.id)+'/')
        else:
            response = redirect('/error/')
            return response
    else:
        return redirect('/')
        

class VistaEditarEvento(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    # specify the model you want to use
    model = Evento
    template_name="editar_evento.html"
    # specify the fields
    form_class = FiestaEditForm
    
    def test_func(self):
        return Empresa.objects.filter(user = self.request.user.id)
    
    def form_valid(self, form):
        #Generar Salt
        salt = proyecto.qr.generate_salt()
        #Obtener Empresa creadora de la Fiesta
        empresa = Empresa.objects.get(user = self.request.user)
        #Crear datos para el mapa
        locator = Nominatim(user_agent='proyecto')
        location = locator.geocode(form.cleaned_data["ubicacion"] + ', Sevilla, España')
        if(location == None):
            messages.add_message(self.request,messages.WARNING,message="Esa dirección no existe")
            return render (self.request, 'editar_evento.html', {'form': form})
        latitud = location.latitude
        longitud = location.longitude
        evento = form.save(commit=False) 
        #Evita que la edición del evento establezca una ubicacion de una fiesta en curso
        ev = Evento.objects.filter(ubicacion = form.cleaned_data["ubicacion"], estado = 'E')
        res = []
        for e in ev:
            if(e.id != evento.id):
                res.append(e)
        print(len(res))
        if(len(res) != 0):
            messages.add_message(self.request,messages.WARNING,message="Ya hay una fiesta en curso aquí!")
            return render (self.request, 'editar_evento.html', {'form': form})
        #Evita que la edición del evento establezca un nombre de una fiesta en curso
        ev = Evento.objects.filter(nombre = form.cleaned_data["nombre"], estado = 'E')
        res = []
        for e in ev:
            if(e.id != evento.id):
                res.append(e)
        print(len(res))
        if(len(res) != 0):
            messages.add_message(self.request,messages.WARNING,message="Ya hay una fiesta en curso con ese nombre!")
            return render (self.request, 'editar_evento.html', {'form': form})
        evento.salt = salt
        evento.empresa = empresa
        evento.latitud = latitud
        evento.longitud = longitud
        #Al editarse, un evento sigue en curso. Pasará a acabado en una comprobación previa al listado
        evento.estado = 'E'
        evento.save()
        response = redirect('/empresa/{}/'.format(self.request.user.id))
        return response
 
@login_required       
def crear_fiesta(request):
    #Solo las Empresas tienen acceso
    acceso = Empresa.objects.filter(user = request.user.id)
    if(acceso):
        if request.method == 'POST':
            form = proyecto.forms.FiestaForm(request.POST, request.FILES)
            if form.is_valid():
                #Generar Salt
                salt = proyecto.qr.generate_salt()
                #Obtener Empresa creadora de la Fiesta
                empresa = Empresa.objects.get(user =request.user)
                #Crear datos para el mapa
                locator = Nominatim(user_agent='proyecto')
                location = locator.geocode(form.cleaned_data["ubicacion"] + ', Sevilla, España')
                #En caso que GeoPy no encuentre esa dirección, se vuelve al form avisando del error
                if(location == None):
                    messages.add_message(request,messages.WARNING,message="Esa dirección no existe")
                    return render (request, 'crear_evento.html', {'form': form})
                latitud = location.latitude
                longitud = location.longitude
                #Crear objeto de la Fiesta y guardarlo
                evento = form.save(commit=False)
                evento.salt = salt
                evento.empresa = empresa
                evento.latitud = latitud
                evento.longitud = longitud
                #Al crear, un evento está por defecto En Curso
                evento.estado = 'E'
                evento.save()
                response = redirect('/empresa/{}/'.format(request.user.id))
                return response
            else:
                return render (request, 'crear_evento.html', {'form': form})
        else:
           form = proyecto.forms.FiestaForm()
           return render(request, 'crear_evento.html', {'form':form})
    else:
           return redirect('/')

class Entradas(LoginRequiredMixin, View):
    def get(self, request, id):
        #Solo los Clientes tienen acceso
        acceso = Cliente.objects.filter(user = request.user.id)
        if(acceso):
            print('El id es'+id)
            entrada = Entrada.objects.get(id=id)
            if request.method == 'POST':
                id = request.POST.get('id')
            print(entrada)
            return render(request,'detalles_evento.html', {"entrada":entrada})
        else:
            return redirect('/')

@login_required
def vender(request, evento_id):
    #Solo los Clientes tienen acceso
    acceso = Cliente.objects.filter(user = request.user.id)
    if(acceso):
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
                poner_venta(request,evento,cliente,fechLimite)
                proyecto.notificaciones.send_notificacion(usuario.id, "Se ha puesta a la venta una entrada para " + evento.nombre)
            return redirect(ver_evento, evento_id=evento.id)
        else:
            form = proyecto.forms.TransactionForm()
            return render(request, 'transaccion.html', {'form':form, 'id':evento_id})
    else:
        return redirect('/')

@login_required
def orden_comprar(request, evento_id):
    #Solo los Clientes tienen acceso
    acceso = Cliente.objects.filter(user = request.user.id)
    if(acceso):
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
                poner_compra(request,evento, cliente, fechLimite)
                proyecto.notificaciones.send_notificacion(usuario.id, "Se ha creado una orden de compra para " + evento.nombre)
            return redirect(ver_evento, evento_id=evento.id)
        else:
            form = proyecto.forms.TransactionForm()
            return render(request, 'transaccion.html', {'form':form, 'id':evento_id})
    else:
        return redirect('/')

@login_required    
def cancelar_transaccion(request, evento_id):
    #Solo los Clientes tienen acceso
    acceso = Cliente.objects.filter(user = request.user.id)
    if(acceso):
        o_user = User.objects.get(id=request.user.id)
        evento = Evento.objects.get(id=evento_id)
        cliente = Cliente.objects.get(user = o_user)
        transaccion = Transaccion.objects.filter(cliente = cliente, evento = evento, done = False).exclude(tipo = 'N').first()
        proyecto.transacciones.cancelar_transaccion(transaccion)
        proyecto.notificaciones.send_notificacion(o_user.id, "Se ha concelado la venta de la entrada para " + evento.nombre)
        return redirect(ver_evento, evento_id=evento.id)
    else:
        return redirect('/')

@login_required
def compra_directa(request, evento_id):
    #Solo los Clientes tienen acceso
    acceso = Cliente.objects.filter(user = request.user.id)
    if(acceso):
        o_user = User.objects.get(id=request.user.id)
        cliente = Cliente.objects.get(user = o_user)
        evento = Evento.objects.get(id=evento_id)
        create_entrada(request,cliente,evento)
        proyecto.notificaciones.send_notificacion(o_user.id, "Se ha comprado una entrada para " + evento.nombre)
        return redirect(ver_evento, evento_id=evento.id)
    else:
        return redirect('/')

@login_required
def recargar_saldo(request, id):
    #Solo los Clientes tienen acceso
    acceso = Cliente.objects.filter(user = request.user.id)
    if(acceso):
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
                return render(request, 'saldo_opciones.html', {'form':form})
        else:
            form = proyecto.forms.PaypalAmountForm()
            return render(request, 'saldo_opciones.html', {'form':form})
    else:
        return redirect('/')
        
@csrf_exempt
def payment_done(request):
    global rec
    o_user = User.objects.get(id=request.user.id)
    cliente = Cliente.objects.get(user = o_user)
    
    cliente.saldo += rec
    cliente.save()
    proyecto.notificaciones.send_notificacion(o_user.id, "Se ha recargado el saldo de manera satisfactoria")
    return render(request, 'saldo_exito.html', {'cantidad': rec, 'total': cliente.saldo})

@csrf_exempt
def payment_canceled(request):
    return render(request, 'saldo_cancelado.html')

class NotificacionesView(LoginRequiredMixin, View):
    def get(self, request):
        proyecto.notificaciones.set_read_notificaciones(request.user.id)
        notificaciones = proyecto.notificaciones.get_notificaciones(request.user.id)
        return render(request,'notificaciones.html', {"notificaciones":notificaciones})

@login_required    
def borra_notificacion(request, notificacion_id):
    o_user = User.objects.get(id=request.user.id)
    proyecto.notificaciones.delete_notificacion(notificacion_id)
    return NotificacionesView.as_view()(request)