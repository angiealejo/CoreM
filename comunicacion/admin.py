# -*- coding: utf-8 -*-

# Librerias django
from django.contrib import admin

# Modelos:
from .models import Mensaje


@admin.register(Mensaje)
class AdminMensaje(admin.ModelAdmin):
    list_display = (
        'pk',
        'usuario',
        'texto',
        'created_date',
    )
