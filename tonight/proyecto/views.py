from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model
from proyecto.models import Cliente, Empresa

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
            response = redirect('/index2/')
            return response
        if cliente_exists:
            response = redirect('/index/')
            return response

class ErrorVista(TemplateView):
    template_name = 'error.html'