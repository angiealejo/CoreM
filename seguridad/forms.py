# -*- coding: utf-8 -*-

# Librerias Django
from django.forms import ModelForm
from django.forms import EmailInput
from django.forms import TextInput
from django.forms import Textarea
from django.forms import PasswordInput

# Django Autorizacion
from django.contrib.auth.models import User

# Models
from .models import Profile


class UsuarioCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UsuarioCreateForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].initial = True

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
            'is_staff',
        ]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control input-sm'}),
            'first_name': TextInput(attrs={'class': 'form-control input-sm'}),
            'last_name': TextInput(attrs={'class': 'form-control input-sm'}),
            'email': EmailInput(attrs={'class': 'form-control input-sm'}),
            'password': PasswordInput(attrs={'class': 'form-control input-sm'}),
        }
        labels = {
            'username': 'Cuenta:',
            'first_name': 'Nombre:',
            'last_name': 'Apellidos:',
            'email': 'Email:',
            'password': 'Contraseña:',
            'is_active': 'Activo',
            'is_staff': 'Administrador',
        }


class UsuarioEditForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UsuarioEditForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
            'is_staff',
        ]
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control input-sm'}),
            'last_name': TextInput(attrs={'class': 'form-control input-sm'}),
            'email': EmailInput(attrs={'class': 'form-control input-sm'}),
            'password': PasswordInput(attrs={'class': 'form-control input-sm'}),
        }
        labels = {
            'first_name': 'Nombre:',
            'last_name': 'Apellidos:',
            'email': 'Email:',
            'password': 'Contraseña:',
            'is_active': 'Activo',
            'is_staff': 'Administrador',
        }


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = [
            'user'
        ]
        widgets = {
            'puesto': TextInput(attrs={'class': 'form-control input-sm'}),
            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'fecha_nacimiento': TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'data-date-format': 'yyyy-mm-dd'
                }
            ),
            'comentarios': Textarea(
                attrs={
                    'class': 'form-control input-sm hresize'
                }
            ),
        }
        labels = {
            'clave': 'Clave RH:',
            'puesto': 'Puesto:',
            'fecha_nacimiento': 'Fecha Nacimiento:',
            'comentarios': 'Comentarios:',
            'imagen': 'Imagen:',
            'firma': 'Firma:',
        }
