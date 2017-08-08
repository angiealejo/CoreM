# -*- coding: utf-8 -*-

from django.contrib import admin

# Modelos
from .models import AnexoTexto
from .models import AnexoImagen
from .models import AnexoArchivo


@admin.register(AnexoTexto)
class Texto(admin.ModelAdmin):
    list_display = (
        'equipo',
        'articulo',
        'orden_trabajo',
        'texto',
    )


@admin.register(AnexoImagen)
class ImagenAnexo(admin.ModelAdmin):
    list_display = (
        'equipo',
        'articulo',
        'orden_trabajo',
        'ruta',
        'descripcion',
    )


@admin.register(AnexoArchivo)
class Archivo(admin.ModelAdmin):
    list_display = (
        'equipo',
        'articulo',
        'orden_trabajo',
        'archivo',
        'descripcion',
    )
