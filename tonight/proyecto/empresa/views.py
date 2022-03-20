from django.shortcuts import render, redirect, get_object_or_404
import json
from django.views.generic import View
from django.conf import settings
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from proyecto.models import Empresa, Cliente
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class Vista2(View):
    
    def get(self, request):
        usuario = get_object_or_404(User, id=request.user.id)
        empresa_exists = (Empresa.objects.filter(user = usuario).count() > 0)
        if not empresa_exists:
            response = redirect('/error/')
            return response
        else:
            return render (request, 'index2.html')
        
        

class EmpresaVista(View):
    
    def get(self, request, id):
        usuarios = User.objects.count()
        if int(id) > usuarios:
            response = redirect('/error/')
            return response
        usuario = get_object_or_404(User, id=id)
        empresa_exists = (Empresa.objects.filter(user = usuario).count() > 0)
        if str(request.user.id) != str(id) or not empresa_exists:
            response = redirect('/error/')
            return response
        else:
            empresa = Empresa.objects.get(user=usuario)
            context = {
                'empresa': empresa
            }
        
            return render (request, 'empresa.html', context)