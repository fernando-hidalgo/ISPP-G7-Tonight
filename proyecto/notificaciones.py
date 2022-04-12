from proyecto.models import *
from django.shortcuts import get_object_or_404

def send_notificacion(user_id, mensaje):
    user = get_object_or_404(User, id=user_id)
    notificacion = Notificacion.objects.create(mensaje=mensaje, usuario=user)
    return notificacion

def get_notificaciones(user_id):
    user = get_object_or_404(User, id=user_id)
    notificaciones = Notificacion.objects.filter(usuario=user)
    return notificaciones

def count_unread_notificaciones(user_id):
    user = get_object_or_404(User, id=user_id)
    notificaciones = Notificacion.objects.filter(usuario=user, read = False)
    return len(notificaciones)

def set_read_notificaciones(user_id):
    user = get_object_or_404(User, id=user_id)
    notificaciones = Notificacion.objects.filter(usuario=user, read = False)
    for notificacion in notificaciones:
        notificacion.read = True
        notificacion.save()

def delete_notificacion(notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id)
    notificacion.delete()
