from django.shortcuts import render, get_object_or_404
import json
from django.views.generic import TemplateView, View
from django.conf import settings
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from proyecto.models import Cliente
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class Vista(TemplateView):
    template_name = 'index.html'

class ClienteVista(View):
    
    def get(self, request, id):
        queryset = Cliente.objects.all()
        usuario = request.user.id
        usuario = get_object_or_404(User, id=id)
        print(usuario)
        cliente = Cliente.objects.get(user=usuario)

        context = {
            'cliente': cliente

        }
        
        return render (request, 'cliente.html', context)



    


    