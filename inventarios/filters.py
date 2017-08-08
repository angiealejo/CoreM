# -*- coding: utf-8 -*-

# Django API REST
from rest_framework import filters
from django_filters import CharFilter
from django_filters import DateFilter
# from django_filters import NumberFilter

# Modelos
from .models import Articulo
from .models import MovimientoCabecera
from .models import MovimientoDetalle
from .models import Stock


class ArticuloFilter(filters.FilterSet):

    clave = CharFilter(
        name="clave",
        lookup_expr="icontains"
    )

    clave_jde = CharFilter(
        name="clave_jde",
        lookup_expr="icontains"
    )

    descripcion = CharFilter(
        name="descripcion",
        lookup_expr="icontains"
    )

    class Meta:
        model = Articulo
        fields = [
            'clave',
            'descripcion',
            'tipo',
            'clave_jde',
            'estado',
        ]


class StockFilter(filters.FilterSet):

    cantidad_mayorque = CharFilter(
        name="cantidad",
        lookup_expr="gte"
    )

    cantidad_menorque = CharFilter(
        name="cantidad",
        lookup_expr="lte"
    )

    class Meta:
        model = Stock
        fields = [
            'articulo',
            'almacen',
            'cantidad_mayorque',
            'cantidad_menorque',
        ]


class MovimientoCabeceraFilter(filters.FilterSet):

    fecha_inicio = DateFilter(
        name="fecha",
        lookup_expr="gte"
    )
    fecha_fin = DateFilter(
        name="fecha",
        lookup_expr="lte"
    )
    descripcion = CharFilter(
        name="descripcion",
        lookup_expr="icontains"

    )
    proveedor = CharFilter(
        name="proveedor",
        lookup_expr="icontains"

    )

    class Meta:
        model = MovimientoCabecera
        fields = [
            'almacen_origen',
            'almacen_destino',
            'persona_recibe',
            'persona_entrega',
            'proveedor',
            'estado',
            'tipo',
            'clasificacion',
            'orden_trabajo',
        ]


class MovimientoInventarioFilter(filters.FilterSet):
    fecha_inicio = DateFilter(
        name="cabecera__fecha",
        lookup_expr="gte"
    )
    fecha_fin = DateFilter(
        name="cabecera__fecha",
        lookup_expr="lte"
    )
    cabecera__descripcion = CharFilter(
        name="cabecera__descripcion",
        lookup_expr="icontains"
    )
    cabecera__proveedor = CharFilter(
        name="cabecera__proveedor",
        lookup_expr="icontains"
    )

    class Meta:
        model = MovimientoDetalle

        fields = [
            'articulo',
            'cabecera',
            'cabecera__almacen_destino',
            'cabecera__almacen_origen',
            'cabecera__persona_recibe',
            'cabecera__persona_entrega',
            'cabecera__tipo',
            'cabecera__clasificacion',
            'cabecera__orden_trabajo'
        ]
