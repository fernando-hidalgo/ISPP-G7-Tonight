
from asyncio import events
from proyecto.models import *
import datetime
import proyecto.entrada

def make_transaccion(tr_compradora, tr_vendedora):
    entrada = Entrada.objects.get(evento = tr_compradora.evento, cliente = tr_vendedora.cliente)
    entrada.estado = 'V'
    tr_vendedora.cliente.saldo += tr_vendedora.evento.precio
    tr_compradora.cliente.saldo -= tr_vendedora.evento.precio
    tr_compradora.done = True
    tr_vendedora.done = True
    tr_compradora.save()
    tr_vendedora.save()
    proyecto.entrada.create_entrada(tr_compradora.cliente, tr_vendedora.evento)
    return

def check_transacciones(transaccion):
    if transaccion.tipo == 'V':
        transacciones = Transaccion.objects.filter(evento = transaccion.evento, tipo = 'C', done=False)
        if transacciones.count() > 0:
            transaccion_select = Transaccion.objects.get(id=transacciones.first().id)
            make_transaccion(transaccion_select, transaccion)
    else:
        transacciones = Transaccion.objects.filter(evento = transaccion.evento, tipo = 'V', done=False)
        if transacciones.count() > 0:
            transaccion_select = Transaccion.objects.get(id=transacciones.first().id) 
            make_transaccion(transaccion, transaccion_select)
    return

def poner_venta(evento, cliente, fech):
    """En caso de estar adquirida creamos una transacción y pasamos a el estado En venta"""
    entrada = Entrada.objects.filter(cliente = cliente, evento = evento).first()
    if(entrada.estado == 'A'):
        transaccion = Transaccion.objects.create(tipo='V', fechaAudit=datetime.datetime.now(), fechaLimite=fech, evento=evento, cliente=cliente)
        entrada.estado = 'E'
        entrada.save()
        check_transacciones(transaccion)
    return

def poner_compra(evento, cliente, fech):
    transaccion = Transaccion.objects.create(tipo='C', fechaAudit=datetime.datetime.now(), fechaLimite=fech, evento=evento, cliente=cliente)
    check_transacciones(transaccion)
    return

def vender_entrada(entrada, fech):
    if entrada.status == 'A':
        entrada.status = 'E'
        poner_venta(entrada.evento, entrada.cliente, fech)
    else:
        print("No se puedes poner a la venta entradas que ya estan caducadas, usadas o vendidas")
    
def cancelar_transaccion(trs):
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