# -*- coding: utf-8 -*-

# Django API REST
from rest_framework import filters
from django_filters import DateFilter

# Modelos:
from .models import Programa


class ProgramaFilter(filters.FilterSet):

    fecha_inicio = DateFilter(
        name="fecha",
        lookup_expr="gte"
    )
    fecha_fin = DateFilter(
        name="fecha",
        lookup_expr="lte"
    )

    class Meta:
        model = Programa
        fields = [
            'equipo',
            'periodicidad',
            'fecha_inicio',
            'fecha_fin',
            'esta_activo',
        ]
