from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms
from proyecto.models import Cliente, Empresa, Evento
import datetime
from django.forms import TextInput

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]
        labels = {
            'username': 'Nombre',
            'email': 'Correo',
        }
        help_texts = {
            'username': None,
            'email': None,
        }
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name in ('username', 'email', 'password1', 'password2'):
            self.fields[field_name].help_text = ''


class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
        labels = {
            'username': 'Nombre',
            'email': 'Correo',
            'password': 'Contraseña',
        }
        help_texts = {
            'username': None,
            'email': None,
            'password': None,
        }
        
    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        for field_name in ('username', 'email', 'password1', 'password2'):
            self.fields[field_name].help_text = ''

        
class ClienteModelForm(ModelForm):
    tlf = PhoneNumberField(widget = PhoneNumberPrefixWidget(initial='ES'))
    class Meta:
        model = Cliente
        exclude = ('user', 'saldo')
        fields = ['tlf', "imagen"]
        labels = {
            'tlf': 'Teléfono',
            'imagen': 'Imagen',
        }
        help_texts = {
            'tlf': None,
            'imagen': None,
        }
    def __init__(self, *args, **kwargs):
        super(ClienteModelForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = True
        self.fields['tlf'].required = True
        for field_name in ('tlf', 'imagen'):
            self.fields[field_name].help_text = ''

class EmpresaModelForm(ModelForm):
    tlf = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial='ES')
    )
    class Meta:
        model = Empresa
        exclude = ('user',)
        fields = ['tlf','cif', "imagen",]
        labels = {
            'tlf': 'Número de teléfono',
            'imagen': 'Imagen',
            'cif': 'CIF',
        }
    def __init__(self, *args, **kwargs):
        super(EmpresaModelForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = True
        self.fields['imagen'].help_text = ''

class NumberInput(forms.NumberInput):
    input_type = 'number'

class PaypalAmountForm(forms.Form):
    cantidad = forms.IntegerField(widget=NumberInput, label="Cantidad")

class DatePickerInput(forms.DateInput):
        input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'

class TransactionForm(forms.Form):
    dia = forms.DateField(widget=DatePickerInput, label="Día")
    hora = forms.TimeField(widget=TimePickerInput, label="Hora")

def present_or_future_date(value):
    if value < datetime.date.today():
        raise forms.ValidationError("Viajar en el tiempo no es una opción!")
    return value

def above_zero(value):
    if value <= 0:
        raise forms.ValidationError("Este campo debe ser mayor que 0!")
    return value

def repeated_ongoing_name(value):
    repeated = False
    eventos = Evento.objects.all()
    for evento in eventos:
        if(evento.nombre == value): #Queda añadir el estado
            repeated = True
    if(repeated):
        raise forms.ValidationError("Ya hay una fiesta en curso con ese nombre!")
    return value

def repeated_ongoing_place(value):
    repeated = False
    eventos = Evento.objects.all()
    for evento in eventos:
        if(evento.ubicacion == value):  #Queda añadir el estado
            repeated = True
    if(repeated):
        raise forms.ValidationError("Ya hay una fiesta en curso aquí!")
    return value
    
class FiestaForm(ModelForm):
    #dia = forms.DateField(widget=DatePickerInput, label="Día", validators=[present_or_future_date])
    #hora = forms.TimeField(widget=TimePickerInput, label="Hora")
    precioEntrada = forms.IntegerField(widget=NumberInput(attrs={'placeholder':'Cantidad >=0'}), label="Precio", validators=[above_zero])
    totalEntradas = forms.IntegerField(widget=NumberInput(attrs={'placeholder':'Cantidad >=0'}), label="Total Entradas", validators=[above_zero])
    nombre = forms.CharField(label="Nombre", validators=[repeated_ongoing_name])
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")
    ubicacion = forms.CharField(label="Ubicación", validators=[repeated_ongoing_place])
    imagen = forms.ImageField(widget=forms.FileInput(), label="Imágen")
    
    class Meta:
        model = Evento
        exclude = ('salt','latitud','longitud','empresa')
        
def repeated_ongoing_name_ignore_self(value):
    eventos = Evento.objects.all()
    cont = 0
    for evento in eventos:
        if(evento.nombre == value): #Queda añadir el estado
            cont += 1  
    #Si vale 2, significa que se ha encontrado a si mismo y a otro mas 
    if(cont >=2):
        raise forms.ValidationError("Ya hay una fiesta en curso con ese nombre!")
    return value

def repeated_ongoing_place_ignore_self(value):
    eventos = Evento.objects.all()
    cont = 0
    for evento in eventos:
        if(evento.ubicacion == value):  #Queda añadir el estado
            cont += 1 
    #Si vale 2, significa que se ha encontrado a si mismo y a otro mas 
    if(cont >=2):
        raise forms.ValidationError("Ya hay una fiesta en curso aquí!")
    return value
        
class FiestaEditForm(ModelForm):
    #dia = forms.DateField(widget=DatePickerInput, label="Día", validators=[present_or_future_date])
    #hora = forms.TimeField(widget=TimePickerInput, label="Hora")
    precioEntrada = forms.IntegerField(widget=NumberInput(attrs={'placeholder':'Cantidad >=0'}), label="Precio", validators=[above_zero])
    totalEntradas = forms.IntegerField(widget=NumberInput(attrs={'placeholder':'Cantidad >=0'}), label="Total Entradas", validators=[above_zero])
    nombre = forms.CharField(label="Nombre", validators=[repeated_ongoing_name_ignore_self])
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")
    ubicacion = forms.CharField(label="Ubicación", validators=[repeated_ongoing_place_ignore_self])
    
    class Meta:
        model = Evento
        exclude = ('salt','latitud','longitud','empresa')
        fields = ["fecha","precioEntrada","totalEntradas","nombre","descripcion","ubicacion", "imagen",]
        labels = {
            'imagen': 'Imagen',
        }
        widgets = {
            'fecha': TextInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'}),
        }