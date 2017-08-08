# -*- coding: utf-8 -*-

# Librerias django
from django.contrib import admin

# Modelos:
from .models import Programa


@admin.register(Programa)
class AdminPrograma(admin.ModelAdmin):
    list_display = (
        'equipo',
        'descripcion',
        'periodicidad',
        'frecuencia',
        'fecha',
        'esta_activo',
        'observaciones',
    )
