# -*- coding: utf-8 -*-

# Librerias Django:
from django.contrib import admin

# Modelos:
from .models import Contrato
from .models import Empresa
from .models import Turno

# Historia
from simple_history.admin import SimpleHistoryAdmin


@admin.register(Contrato)
class ContratoUbicacion(SimpleHistoryAdmin):
    list_display = (
        'pk',
        'clave',
        'nombre',
        'descripcion',
        'cliente',
        'numero',
        'region',
        'estado',
        'created_date',
        'created_by',
        'updated_date',
        'updated_by',
    )


@admin.register(Empresa)
class Empresa(admin.ModelAdmin):
    list_display = (
        'pk',
        'clave',
        'descripcion',
        'logo',
    )


@admin.register(Turno)
class Turno(SimpleHistoryAdmin):
    list_display = (
        'pk',
        'clave',
        'descripcion',
        'hora_inicio',
        'hora_fin',
        'created_by',
        'created_date',
        'updated_by',
        'updated_date',
    )
