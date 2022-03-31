from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from proyecto.models import Cliente
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms

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

    tlf = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial='ES')
    )
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