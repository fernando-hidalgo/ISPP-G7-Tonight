from django.contrib import admin
from proyecto.models import Cliente,Evento,Entrada,Empleado,Empresa
# Register your models here.
admin.site.register(Evento)
admin.site.register(Cliente)
admin.site.register(Entrada)
admin.site.register(Empresa)
admin.site.register(Empleado)