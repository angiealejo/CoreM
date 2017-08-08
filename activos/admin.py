# -*- coding: utf-8 -*-

# Librerias Django:
from django.contrib import admin

# Modelos:
from .models import Equipo
from .models import Ubicacion
# from .models import Asignacion
from .models import Odometro
from .models import Medicion
from .models import UdmOdometro
from .models import TipoOdometro
from .models import TipoEquipo

from administracion.models import Contrato

# Historia
from simple_history.admin import SimpleHistoryAdmin

# Import-Export
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import Widget
from import_export.widgets import ForeignKeyWidget


class EquipoResource(resources.ModelResource):

    contrato_nombre = fields.Field(
        column_name='contrato_nombre',
        attribute="contrato",
        widget=ForeignKeyWidget(Contrato, 'clave')
    )

    ubicacion_nombre = fields.Field(
        column_name='ubicacion_nombre',
        attribute="ubicacion",
        widget=ForeignKeyWidget(Ubicacion, 'clave')
    )

    padre_nombre = fields.Field(
        column_name='padre_nombre',
        attribute="padre",
        widget=ForeignKeyWidget(Equipo, 'tag')
    )

    class Meta:
        model = Equipo
        exclude = ('id', )
        fields = (
            'tag',
            'descripcion',
            'estado',
            'contrato_nombre',
            'ubicacion_nombre',
            'padre_nombre',
        )
        import_id_fields = ['tag']


@admin.register(Equipo)
class AdminEquipo(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = EquipoResource
    list_display = (
        'id',
        'tag',
        'descripcion',
        'serie',
        'especialidad',
        'estado',
        'tipo',
        'padre',
        'ubicacion',
        'sistema',
        'cliente',
        'responsable',
        'created_date',
        'updated_date',
    )


@admin.register(Ubicacion)
class AdminUbicacion(admin.ModelAdmin):
    list_display = (
        'clave',
        'descripcion',
        'created_date',
        'updated_date',
    )

# @admin.register(Sistema)
# class AdminUbicacion(admin.ModelAdmin):
#     list_display = (
#         'clave',
#         'descripcion',
#         'created_date',
#         'created_by',
#         'updated_date',
#         'updated_by',
#     )


class UdmOdometroResource(resources.ModelResource):

    class Meta:
        model = UdmOdometro
        exclude = ('id',)
        fields = (
            'clave',
            'descripcion'
        )
        import_id_fields = ['clave']


@admin.register(UdmOdometro)
class AdminUdmOdometro(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = UdmOdometroResource
    list_display = (
        'clave',
        'descripcion',
        'created_date',
        'updated_date',
    )


class OdometroResource(resources.ModelResource):

    tipo_odometro = fields.Field(
        column_name='tipo',
        attribute="tipo",
        widget=ForeignKeyWidget(TipoOdometro, 'clave')
    )
    udm = fields.Field(
        column_name='udm',
        attribute="udm",
        widget=ForeignKeyWidget(UdmOdometro, 'clave')
    )

    class Meta:
        model = Odometro
        exclude = ('id', )
        fields = (
            'clave',
            'descripcion',
            'udm',
            'tipo_odometro',
            'acumulado',
            'clasificacion',
        )
        import_id_fields = ['clave']


@admin.register(Odometro)
class Odometro(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = OdometroResource
    list_display = (
        'id',
        'clave',
        'descripcion',
        'udm',
        'tipo',
        'acumulado',
        'clasificacion',
        'esta_activo',
        'created_date',
        'updated_date',
    )


class MedicionResource(resources.ModelResource):

    odometro = fields.Field(
        column_name='odometro',
        attribute="odometro",
        widget=ForeignKeyWidget(Odometro, 'clave')
    )
    equipo = fields.Field(
        column_name='equipo',
        attribute="equipo",
        widget=ForeignKeyWidget(Equipo, 'tag')
    )

    class Meta:
        model = Medicion
        exclude = ('id', )
        fields = (
            'odometro',
            'equipo',
            'fecha',
            'lectura',
            'observaciones',
            'created_date',
            'updated_date',
        )


@admin.register(Medicion)
class Medicion(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MedicionResource
    list_display = (
        'odometro',
        'equipo',
        'fecha',
        'lectura',
        'observaciones',
        'created_date',
        'created_by',
        'updated_date',
        'updated_by'
    )


class TipoOdometroResource(resources.ModelResource):

    class Meta:
        model = TipoOdometro
        exclude = ('id', )
        fields = (
            'clave',
            'descripcion',
        )
        import_id_fields = ['clave']


@admin.register(TipoOdometro)
class TipoOdometroAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = TipoOdometroResource
    list_display = (
        'id',
        'clave',
        'descripcion',
        'created_date',
        'updated_date',
    )


class TipoEquipoResource(resources.ModelResource):

    class Meta:
        model = TipoEquipo
        exclude = ('id', )
        fields = (
            'clave',
            'descripcion',
        )
        import_id_fields = ['clave']


@admin.register(TipoEquipo)
class TipoOEquipoAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = TipoEquipoResource
    list_display = (
        'id',
        'clave',
        'descripcion',
        'created_date',
        'created_by',
        'updated_date',
        'updated_by'
    )
