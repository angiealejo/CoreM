# -*- coding: utf-8 -*-

# Django:
from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from django.forms import Textarea

# Modelos:
from .models import AnexoArchivo
from .models import AnexoImagen
from .models import AnexoTexto


class AnexoTextoForm(ModelForm):

    class Meta:
        model = AnexoTexto
        fields = ['titulo', 'texto']
        widgets = {
            'titulo': TextInput(attrs={'class': 'form-control input-sm'}),
            'texto': Textarea(
                attrs={'class': 'textarea form-control input-sm'}
            )
        }
        labels = {
            'titulo': 'Título',
            'texto': 'Texto',
        }


class AnexoImagenForm(ModelForm):

    class Meta:
        model = AnexoImagen
        fields = ['descripcion', 'ruta']
        labels = {
            'ruta': 'Imagen',
            'descripcion': 'Descripción o comentario',
        }
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control'})
        }

    def validar_extension(self):
        diccionario = self.cleaned_data

        imagen = diccionario.get('ruta')
        if (not imagen.endswith('.png') and
            not imagen.endswith('.jpg') and
                not imagen.endswith('.jpeg')):

            raise forms.ValidationError("Error")
        else:
            return imagen


class AnexoArchivoForm(ModelForm):

    class Meta:
        model = AnexoArchivo
        fields = ['descripcion', 'archivo']
        labels = {
            'descripcion': 'Descripción',
            'archivo': 'Archivo',
        }
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control'})
        }
