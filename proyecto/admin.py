from django.contrib import admin
from .models import Cliente, Empresa, Empleado, Evento, Entrada, Transaccion

from .models import Empresa, Evento

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Empresa)
admin.site.register(Empleado)
admin.site.register(Evento)
admin.site.register(Entrada)
admin.site.register(Transaccion)