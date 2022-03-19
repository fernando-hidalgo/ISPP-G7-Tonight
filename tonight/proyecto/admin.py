from django.contrib import admin

# Register your models here.

def venderEntradas(self, request, *args, **kwargs):
    #print("hola mundo")
    # asignamos una entrada disponible a un usuario
    nombreEvento = input("evento al que quiero ir:")
    evento_list = request.data.get('eventos') #conjunto de todos los eventos
    for e in evento_list:
        if(nombreEvento == e.nombre):
            evento = request.data.get('e') # nos quedamos con el evento coincidente
            entradas = request.data.get('entrada') # conjunto de todas las entradas
            for en in entradas:
                if en.evento == evento:
                    entradaTratada = en
                    if entradaTratada.estado == 'STATUS.E'
                    entradaAdquirida = en
                    # cargar los campos de entrada

    
