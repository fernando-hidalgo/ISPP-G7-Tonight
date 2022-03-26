
from proyecto.models import *
import datetime
import proyecto.entrada

def make_transaccion(tr_compradora, tr_vendedora):
    entrada = Entrada.objects.get(evento = tr_compradora.evento, cliente = tr_vendedora.cliente)
    entrada.status = 'V'
    tr_vendedora.cliente.saldo += tr_vendedora.evento.precio
    tr_compradora.cliente.saldo -= tr_vendedora.evento.precio
    tr_compradora.done = True
    tr_vendedora.done = True
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
    transaccion = Transaccion.objects.create(tipo='V', fechaAudit=datetime.datetime.now(), fechaLimite=fech, evento=evento, cliente=cliente)
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
    
def ordenar_entrada(cliente, evento, fech):
    poner_compra(evento, cliente, fech)

def cancelar_venta(entrada, transaccion):
    entrada.status = 'A'
    transaccion.delete()
    return