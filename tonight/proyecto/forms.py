from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm
from proyecto.models import Cliente

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }


class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password': 'Contraseña',
        }


class ClienteModelForm(ModelForm):
    class Meta:
        model = Cliente
        exclude = ('user', 'saldo')
        fields = ['tlf', "imagen"]
        labels = {
            'tlf': 'Número de teléfono',
            'imagen': 'Imagen',
        }