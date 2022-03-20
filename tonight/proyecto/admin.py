from django.contrib import admin

from .models import Empresa, Evento

# Register your models here.
admin.site.register(Evento)
admin.site.register(Empresa)