
from asyncio import events
from proyecto.models import *
import datetime
import proyecto.entrada
from django.contrib import messages


def make_transaccion(request, tr_compradora, tr_vendedora):
    print("Se esta haciendo el intercambio")
    entrada = Entrada.objects.get(evento = tr_compradora.evento, cliente = tr_vendedora.cliente)
    evento = entrada.evento
    evento.totalEntradas = 1
    evento.save()
    print(evento.totalEntradas)
    proyecto.entrada.create_entrada(request, tr_compradora.cliente, evento)
    entrada.estado = 'V'
    tr_vendedora.cliente.saldo += tr_vendedora.evento.precioEntrada
    tr_compradora.done = True
    tr_vendedora.done = True
    tr_compradora.save()
    tr_vendedora.save()
    evento.totalEntradas = 0
    evento.save()
    entrada.save()
    print(evento.totalEntradas)
    print(evento)
    print(tr_vendedora.evento)
    return

def check_transacciones(request, transaccion):
    caduca_transacciones()
    if transaccion.tipo == 'V':
        transacciones = Transaccion.objects.filter(evento = transaccion.evento, tipo = 'C', done=False)
        if transacciones.count() > 0:
            transaccion_select = Transaccion.objects.get(id=transacciones.first().id)
            make_transaccion(request, transaccion_select, transaccion)
    else:
        print("Mirando si hay transacciones en venta para este evento")
        transacciones = Transaccion.objects.filter(evento = transaccion.evento, tipo = 'V', done=False)
        print(transacciones)
        if transacciones.count() > 0:
            print("Encontrada transaccion de venta para esta compra")
            transaccion_select = Transaccion.objects.get(id=transacciones.first().id) 
            make_transaccion(request, transaccion, transaccion_select)
    return

def poner_venta(request, evento, cliente, fech):
    """En caso de estar adquirida creamos una transacción y pasamos a el estado En venta"""
    entrada = Entrada.objects.filter(cliente = cliente, evento = evento).first()
    if(entrada.estado == 'A'):
        transaccion = Transaccion.objects.create(tipo='V', fechaAudit=datetime.datetime.now(), fechaLimite=fech, evento=evento, cliente=cliente)
        entrada.estado = 'E'
        entrada.save()
        check_transacciones(request, transaccion)
    return

def poner_compra(request, evento, cliente, fech):
    if cliente.saldo - evento.precioEntrada >= 0:
        if evento.estado == 'A':
            messages.info(request, 'Este evento ya ha acabado')
            return False
        else:
            transaccion = Transaccion.objects.create(tipo='C', fechaAudit=datetime.datetime.now(), fechaLimite=fech, evento=evento, cliente=cliente)
            check_transacciones(request, transaccion)
            return True
    else:
        messages.info(request, 'No tienes saldo disponible!')
        return False

def vender_entrada(request, entrada, fech):
    if entrada.status == 'A':
        entrada.status = 'E'
        poner_venta(request, entrada.evento, entrada.cliente, fech)
    else:
        messages.info(request, 'No se puedes poner a la venta entradas que ya estan caducadas, usadas o vendidas!')
    
def cancelar_transaccion(trs):
    caduca_transacciones()
    if trs.tipo == 'V':
        entrada = Entrada.objects.filter(cliente = trs.cliente, evento = trs.evento).first()
        entrada.estado = "A"
        entrada.save()
        trs.tipo = 'N'
        trs.save()
    else:
        trs.tipo = 'N'
        trs.save()
    return

def caduca_transacciones():
    trs = Transaccion.objects.filter(done=False, tipo='C' or 'V')
    for tr in trs:
        ahora = datetime.datetime.now()
        if tr.fechaLimite <= ahora:
            tr.tipo = "N"
            tr.save()
        elif (tr.evento.fecha + datetime.timedelta(days=1)) <= ahora:
            tr.tipo = "N"
            tr.save()
    return