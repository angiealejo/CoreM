# -*- coding: utf-8 -*-

# Django:
from django.forms import ModelForm
from django.forms import TextInput
from django.forms import Select
from django.forms import Textarea
from django.forms import ImageField

# Modelos
from .models import Contrato
from .models import Empresa

# ----------------- CONTRATO ----------------- #


class ContratoFiltersForm(ModelForm):

    class Meta:
        model = Contrato
        fields = {
            'clave',
            'nombre',
            'cliente',
            'numero',
            'region',
            'estado',
        }
        widgets = {

            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'nombre': TextInput(attrs={'class': 'form-control input-sm'}),
            'cliente': TextInput(attrs={'class': 'form-control input-sm'}),
            'numero': TextInput(attrs={'class': 'form-control input-sm'}),
            'region': TextInput(attrs={'class': 'form-control input-sm'}),
            'estado': Select(attrs={'class': 'form-control input-sm select2'}),
        }


class ContratoForm(ModelForm):

    class Meta:
        model = Contrato
        fields = '__all__'
        exclude = [
            'created_date',
            'created_by',
            'updated_date',
            'updated_by',
        ]
        widgets = {

            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'nombre': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': Textarea(attrs={'class': 'form-control input-sm'}),
            'cliente': TextInput(attrs={'class': 'form-control input-sm'}),
            'numero': TextInput(attrs={'class': 'form-control input-sm'}),
            'region': TextInput(attrs={'class': 'form-control input-sm'}),
            'estado': Select(attrs={'class': 'form-control input-sm select2'}),
        }


class EmpresaForm(ModelForm):

    class Meta:
        model = Empresa
        fields = [
            'clave',
            'logo',
            'descripcion'
        ]
        widgets = {

            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
        }
