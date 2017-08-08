# -*- coding: utf-8 -*-

# Librerias django
from django.contrib import admin

# Historia
from simple_history.admin import SimpleHistoryAdmin

# Modelos:
from .models import OrdenTrabajo
from .models import Actividad
from .models import ActividadDetalle
from .models import ManoObra
from .models import Material
from .models import ServicioExterno
from .models import SolicitudCompraEncabezado
from .models import SolicitudCompraDetalle


@admin.register(OrdenTrabajo)
class AdminOrdenTrabajo(SimpleHistoryAdmin):
    search_fields = (
        'id',
        'descripcion',
        'especialidad',
        'codigo_reporte',
        'tipo',
        'estado',
        'permiso',
        'observaciones',
        'motivo_cancelacion',
    )
    list_display = (
        'id',
        'equipo',
        'descripcion',
        'especialidad',
        'codigo_reporte',
        'tipo',
        'estado',
        'responsable',
        'solicitante',
        'permiso',
        'fecha_estimada_inicio',
        'fecha_estimada_fin',
        'fecha_real_inicio',
        'fecha_real_fin',
        'observaciones',
        'motivo_cancelacion',
        'es_template',
    )


@admin.register(Actividad)
class AdminActividad(SimpleHistoryAdmin):
    list_display = (
        'orden',
        'numero',
        'descripcion',
        'horas_estimadas',
        'horas_reales',
    )


@admin.register(ActividadDetalle)
class AdminActividadDetalle(SimpleHistoryAdmin):
    list_display = (
        'comentarios',
        'imagen',
    )


@admin.register(ManoObra)
class AdminManoObra(SimpleHistoryAdmin):
    list_display = (
        'orden',
        'empleado',
        'descripcion',
        'fecha_inicio',
        'fecha_fin',
        'horas_estimadas',
        'horas_reales',
    )


@admin.register(Material)
class AdminMaterial(SimpleHistoryAdmin):
    list_display = (
        'orden',
        'articulo',
        'almacen',
        'cantidad_estimada',
        'cantidad_real',
    )


@admin.register(ServicioExterno)
class AdminServicioExterno(SimpleHistoryAdmin):
    list_display = (
        'orden',
        'clave_jde',
        'descripcion',
    )


@admin.register(SolicitudCompraEncabezado)
class AdminSolicitudCompraEncabezado(admin.ModelAdmin):
    list_display = (
        'pk',
        'descripcion',
        'comentarios',
        'estado',
        'solicitante',
        'created_by',
        'updated_by',
        'created_date',
        'updated_date',
    )


@admin.register(SolicitudCompraDetalle)
class AdminSolicitudCompraDetalle(admin.ModelAdmin):
    list_display = (
        'pk',
        'encabezado',
        'articulo',
        'cantidad',
        'comentarios',
        'created_date',
    )
