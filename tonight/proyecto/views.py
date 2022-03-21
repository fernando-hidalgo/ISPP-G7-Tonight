from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model
from proyecto.models import Cliente, Empresa
import json
from django.conf import settings
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

User = get_user_model()

# Create your views here.
def index(request): 
    return render(request,'error.html')

class InicioVista(View):
    def get(self, request):
        usuario = get_object_or_404(User, id=request.user.id)
        empresa_exists = (Empresa.objects.filter(user = usuario).count() > 0)
        cliente_exists = (Cliente.objects.filter(user = usuario).count() > 0)
        if empresa_exists:
            response = redirect('/welcome_bussines/')
            return response
        if cliente_exists:
            response = redirect('/welcome_client/')
            return response

class ErrorVista(TemplateView):
    template_name = 'error.html'

class Vista(View):
    
    def get(self, request):

        usuario = get_object_or_404(User, id=request.user.id)
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

class ClienteVista(View):
    
    def get(self, request, id):
        usuarios = User.objects.count()
        ## if int(id) > usuarios:
        ##    response = redirect('/error/')
        ##    return response
        usuario = get_object_or_404(User, id=id)
        cliente_exists = (Cliente.objects.filter(user = usuario).count() > 0)
        if str(request.user.id) != str(id) or not cliente_exists:
            response = redirect('/error/')
            return response
        else:
            cliente = Cliente.objects.get(user=usuario)

            context = {
                'cliente': cliente
            }
        
            return render (request, 'cliente.html', context)
        
class Vista2(View):
    
    def get(self, request):
        usuario = get_object_or_404(User, id=request.user.id)
        empresa_exists = (Empresa.objects.filter(user = usuario).count() > 0)
        if not empresa_exists:
            response = redirect('/error/')
            return response
        else:
            return render (request, 'welcome_bussines.html')
        
        

class EmpresaVista(View):
    
    def get(self, request, id):
        usuarios = User.objects.count()
        ##if int(id) > usuarios:
        ##    response = redirect('/error/')
        ##    return response
        usuario = get_object_or_404(User, id=id)
        empresa_exists = (Empresa.objects.filter(user = usuario).count() > 0)
        if str(request.user.id) != str(id) or not empresa_exists:
            response = redirect('/error/')
            return response
        else:
            empresa = Empresa.objects.get(user=usuario)
            ##eventos = Evento.objects.filter(empresa=empresa)
            context = {
                'empresa': empresa,
                ##'eventos': eventos
            }
        
            return render (request, 'empresa.html', context)
