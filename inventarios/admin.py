# -*- coding: utf-8 -*-

# Librerias Django:
from django.contrib import admin

# Modelos:
from .models import UdmArticulo
from .models import Articulo
from .models import SeccionAlmacen
from .models import Almacen
from .models import Stock
from .models import MovimientoCabecera
from .models import MovimientoDetalle

# Historia
from simple_history.admin import SimpleHistoryAdmin

# Import-Export
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import Widget
from import_export.widgets import ForeignKeyWidget


class ArticuloResource(resources.ModelResource):

    udm_clave = fields.Field(
        column_name='udm_clave',
        attribute="udm",
        widget=ForeignKeyWidget(UdmArticulo, 'clave')
    )

    class Meta:
        model = Articulo
        # exclude = ('id', )
        fields = (
            'id',
            'udm_clave',
            'descripcion',
            'estado',
            'tipo',
            'clave_jde',
            'marca',
            'modelo',
            'numero_parte',
            'stock_seguridad',
            'stock_minimo',
            'stock_maximo',
        )
        import_id_fields = ['id']


@admin.register(Articulo)
class AdminArticulo(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ArticuloResource
    search_fields = ('clave', 'id', 'descripcion')
    list_display = (
        'id',
        'clave',
        'descripcion',
        'estado',
        'tipo',
        'imagen',
        'udm',
        'observaciones',
        'marca',
        'modelo',
        'numero_parte',
        'stock_seguridad',
        'stock_minimo',
        'stock_maximo',
        'clave_jde',
        'url',
        'created_date',
        'updated_date',
    )


@admin.register(UdmArticulo)
class AdminUdmArticulo(admin.ModelAdmin):
    list_display = (
        'clave',
        'descripcion',
        'created_date',
        'updated_date',
    )


@admin.register(SeccionAlmacen)
class AdminSeccionAlmacen(admin.ModelAdmin):
    list_display = (
        'clave',
        'descripcion',
        'asignado',
    )


@admin.register(Almacen)
class AdminAlmacen(admin.ModelAdmin):
    list_display = (
        'id',
        'clave',
        'descripcion',
        'estado',
        'created_date',
        'updated_date',
    )


class StockResource(resources.ModelResource):

    almacen_id = fields.Field(
        column_name='almacen_id',
        attribute="almacen",
        widget=ForeignKeyWidget(Almacen, 'id')
    )

    almacen_clave = fields.Field(
        column_name='almacen_clave',
        attribute="almacen",
        widget=ForeignKeyWidget(Almacen, 'clave')
    )

    articulo_descripcion = fields.Field(
        column_name='articulo_descripcion',
        attribute="articulo",
        widget=ForeignKeyWidget(Articulo, 'descripcion')
    )

    articulo_id = fields.Field(
        column_name='articulo_id',
        attribute="articulo",
        widget=ForeignKeyWidget(Articulo, 'id')
    )
    articulo_marca = fields.Field(
        column_name='articulo_marca',
        attribute="articulo",
        widget=ForeignKeyWidget(Articulo, 'marca')
    )
    articulo_modelo = fields.Field(
        column_name='articulo_modelo',
        attribute="articulo",
        widget=ForeignKeyWidget(Articulo, 'modelo')
    )
    articulo_numero_parte = fields.Field(
        column_name='articulo_numero_parte',
        attribute="articulo",
        widget=ForeignKeyWidget(Articulo, 'numero_parte')
    )

    class Meta:
        model = Stock
        # exclude = ('id')
        fields = (
            'id',
            'cantidad',
            'almacen_id',
            'almacen_clave',
            'articulo_id',
            'articulo_descripcion',
            'articulo_marca',
            'articulo_modelo',
            'articulo_numero_parte',
        )
        import_id_fields = ['id']


@admin.register(Stock)
class AdminStock(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('almacen__descripcion', 'articulo__descripcion')
    resource_class = StockResource
    list_display = (
        'almacen',
        'articulo',
        'cantidad',
        'created_date',
        'updated_date',
    )


@admin.register(MovimientoCabecera)
class AdminMovientoCabecera(admin.ModelAdmin):
    search_fields = ('id', 'descripcion')
    list_display = (
        'id',
        'fecha',
        'descripcion',
        'almacen_origen',
        'almacen_destino',
        'persona_recibe',
        'persona_entrega',
        'proveedor',
        'estado',
        'tipo',
        'clasificacion',
        'orden_trabajo',
        'created_by',
        'updated_by',
        'created_date',
        'updated_date'
    )


@admin.register(MovimientoDetalle)
class AdminMovimientoDetalle(admin.ModelAdmin):
    search_fields = ['id', 'articulo__descripcion', 'cabecera__descripcion']
    list_display = (
        'id',
        'articulo',
        'cantidad',
        'cabecera',
        'created_by',
        'updated_by',
        'created_date',
        'updated_date'
    )
