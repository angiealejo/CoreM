# -*- coding: utf-8 -*-

# Django API REST
from rest_framework import filters
from django_filters import CharFilter
from django_filters import DateFilter
from django_filters import NumberFilter
from django_filters import Filter

# Modelos
from .models import Equipo
from .models import Odometro
from .models import Medicion


class EquipoFilter(filters.FilterSet):

    tag = CharFilter(
        name="tag",
        lookup_expr="icontains"
    )

    serie = CharFilter(
        name="serie",
        lookup_expr="icontains"
    )

    sistema = CharFilter(
        name="sistema",
        lookup_expr="icontains"
    )

    descripcion = CharFilter(
        name="descripcion",
        lookup_expr="icontains"
    )

    class Meta:
        model = Equipo
        fields = [
            'tag',
            'serie',
            'estado',
            'tipo',
            'padre',
            'sistema',
            'ubicacion',
            'descripcion',
        ]


class EquipoOrdenFilter(filters.FilterSet):

    tag = CharFilter(
        name="tag",
        lookup_expr="icontains"
    )
    descripcion = CharFilter(
        name="descripcion",
        lookup_expr="icontains"
    )

    class Meta:
        model = Equipo
        fields = [
            'id',
            'tag',
            'descripcion'
        ]


class OdometroFilter(filters.FilterSet):

    clave = CharFilter(
        name="clave",
        lookup_expr="icontains"
    )
    descripcion = CharFilter(
        name="descripcion",
        lookup_expr="icontains"
    )
    # udm = CharFilter(
    #     name="udm",
    #     lookup_expr="icontains"
    # )

    class Meta:
        model = Odometro
        fields = [
            'clave',
            'descripcion',
            'udm',
            'tipo',
            'acumulado',

        ]


class MedicionFilter(filters.FilterSet):
    fecha_inicio_ver = CharFilter(
        name="fecha_inicio",
        method="filter_fecha_inicio_ver"
    )
    fecha_fin_ver = CharFilter(
        name="fecha_fin",
        method="filter_fecha_fin_ver"
    )
    fecha_inicio = CharFilter(
        name="fecha_inicio",
        method="filter_fecha_inicio"
    )
    fecha_fin = CharFilter(
        name="fecha_fin",
        method="filter_fecha_fin"
    )
    fecha_exacta = DateFilter(
        name="fecha",
        lookup_expr="contains"
    )
    lectura_minima = NumberFilter(
        name="lectura",
        lookup_expr="gte"
    )
    lectura_maxima = NumberFilter(
        name="lectura",
        lookup_expr="lte"
    )

    class Meta:
        model = Medicion
        fields = [
            'equipo',
            'odometro',
            'odometro__tipo',
            'created_by',
            'updated_by'
        ]

    def filter_fecha_inicio(self, queryset, name, value):

        valor = "{}T00:00:00".format(value)

        if not value:

            return queryset
        else:

            consulta = queryset.filter(fecha__gte=valor)

            return consulta

    def filter_fecha_fin(self, queryset, name, value):

        valor = "{}T23:59:00".format(value)

        if not value:

            return queryset
        else:

            consulta = queryset.filter(fecha__lte=valor)

            return consulta

    def filter_fecha_inicio_ver(self, queryset, name, value):

        valor = "{}".format(value)

        if not value:

            return queryset
        else:

            consulta = queryset.filter(fecha__gte=valor)

            return consulta

    def filter_fecha_fin_ver(self, queryset, name, value):

        valor = "{}".format(value)

        if not value:

            return queryset
        else:

            consulta = queryset.filter(fecha__lte=valor)

            return consulta
