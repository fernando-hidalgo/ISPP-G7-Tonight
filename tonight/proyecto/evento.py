import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model
from proyecto.models import *
from django.contrib.auth.models import User
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth import views as auth_views

def create_entrada_provisional(o_cliente, o_evento):
    entrada = Entrada.objects.create(fechaCompra=datetime.date.today(), 
        fechaCaducidad=datetime.date.today(), 
        estado=1,
        cliente=o_cliente,
        evento=o_evento,
        hash="no_generado"
        )
    print(entrada)
    return entrada

def buy_ticket(o_user, o_evento):
    if o_evento.totalEntradas > 0:
        cliente = Cliente.objects.get(user=o_user)
        if cliente.saldo - o_evento.precioEntrada >= 0:
            o_evento.totalEntradas -= 1
            cliente.saldo -= o_evento.precioEntrada
            create_entrada_provisional(cliente, o_evento)
        else:
            print("pobre")
            #eres pobre asi que fuera
            return
    else:
        print("no hay")
        #no hay entradas asi que fuera
        return
