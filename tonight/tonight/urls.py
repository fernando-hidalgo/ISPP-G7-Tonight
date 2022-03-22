"""tonight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from proyecto import views
from tonight.proyecto import compra_venta

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('eventos/eventos_id/comprar', compra_venta.conprarEntradas),
    #añadir ruta boton
    path('', compra_venta.venderEntradas),
    path('', compra_venta.cancelarVentaEntrada)
]
