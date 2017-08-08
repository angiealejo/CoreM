# -*- coding: utf-8 -*-

# Django API REST
from rest_framework import filters
from django_filters import CharFilter
from django_filters import DateFilter

# Modelos
from .models import OrdenTrabajo
from .models import SolicitudCompraEncabezado


class OrdenTrabajoFilter(filters.FilterSet):

    descripcion = CharFilter(
        name="descripcion",
        lookup_expr="icontains"
    )
    especialidad = CharFilter(
        name="especialidad",
        lookup_expr="icontains"
    )

    created_date_mayorque = CharFilter(name='created_date_mayorque', method='filter_fecha_mayorque')
    created_date_menorque = CharFilter(name='created_date_menorque', method='filter_fecha_menorque')

    class Meta:
        model = OrdenTrabajo
        fields = [
            'id',
            'equipo',
            'descripcion',
            'especialidad',
            'tipo',
            'estado',
            'responsable',
            'solicitante',
            'created_date_mayorque',
            'created_date_menorque',
        ]

    def filter_fecha_mayorque(self, queryset, name, value):

        valor = "{}T00:00:00".format(value)

        if not value:
            return queryset
        else:
            consulta = queryset.filter(created_date__gte=valor)
            return consulta

    def filter_fecha_menorque(self, queryset, name, value):

        valor = "{}T23:59:59".format(value)

        if not value:
            return queryset
        else:
            consulta = queryset.filter(created_date__lte=valor)
            return consulta


class SolicitudCompraEncabezadoFilter(filters.FilterSet):

    fecha_inicio = DateFilter(
        name="created_date",
        lookup_expr="gte"
    )
    fecha_fin = DateFilter(
        name="created_date",
        lookup_expr="lte"
    )
    descripcion = CharFilter(
        name="descripcion",
        lookup_expr="icontains"
    )

    class Meta:
        model = SolicitudCompraEncabezado
        fields = [
            'id',
            'descripcion',
            'estado',
            'solicitante',
            'created_date',
        ]
