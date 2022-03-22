from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model
from proyecto.models import Cliente, Empresa, Evento, Entrada
from django.contrib.auth.models import User
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth import views as auth_views

User = get_user_model()

# Create your views here.

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
