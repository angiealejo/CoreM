# -*- coding: utf-8 -*-

# API REST:
from rest_framework import serializers

# Modelos:
from .models import OrdenTrabajo
from .models import Actividad
from .models import ManoObra
from .models import Material
from .models import ServicioExterno
from .models import ActividadDetalle
from .models import SolicitudCompraEncabezado
from .models import SolicitudCompraDetalle


# ----------------- ORDEN DE TRABAJO ----------------- #

class OrdenTrabajoSerializer(serializers.HyperlinkedModelSerializer):

    equipo = serializers.SerializerMethodField()
    equipo_id = serializers.SerializerMethodField()
    tipo = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    responsable = serializers.SerializerMethodField()
    solicitante = serializers.SerializerMethodField()
    especialidad = serializers.SerializerMethodField()

    class Meta:
        model = OrdenTrabajo
        fields = (
            'url',
            'pk',
            'equipo',
            'equipo_id',
            'descripcion',
            'codigo_reporte',
            'especialidad',
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
            'es_template',
            'created_date',
        )

    def get_responsable(self, obj):

        try:
            return obj.responsable.user.get_full_name()
        except:
            return ""

    def get_solicitante(self, obj):

        try:
            return obj.solicitante.user.get_full_name()
        except:
            return ""

    def get_equipo(self, obj):

        try:
            tag = obj.equipo.tag
            descripcion = obj.equipo.descripcion
            return "(%s) %s" % (tag, descripcion)
        except:
            return ""

    def get_equipo_id(self, obj):

        try:
            return obj.equipo.id
        except:
            return ""

    def get_tipo(self, obj):
        try:
            return obj.get_tipo_display()
        except:
            return ""

    def get_estado(self, obj):
        try:
            return obj.get_estado_display()
        except:
            return ""

    def get_especialidad(self, obj):
        try:
            return obj.get_especialidad_display()
        except:
            return ""


# ----------------- ACTIVIDAD ----------------- #

class ActividadSerializer(serializers.HyperlinkedModelSerializer):

    orden_id = serializers.SerializerMethodField()

    class Meta:
        model = Actividad
        fields = (
            'pk',
            'url',
            'orden',
            'orden_id',
            'numero',
            'descripcion',
            'horas_estimadas',
            'horas_reales',
        )

    def get_orden_id(self, obj):

        try:
            return obj.orden.id
        except:
            return ""


class ActividadDetalleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ActividadDetalle
        fields = (
            'pk',
            'url',
            'actividad',
            'comentarios',
            'imagen',
            'created_by',
            'created_date',
            'updated_date',
        )


# ----------------- MATERIAL ----------------- #

class MaterialSerializer(serializers.HyperlinkedModelSerializer):

    articulo_id = serializers.SerializerMethodField()
    articulo_desc = serializers.SerializerMethodField()
    articulo_udm = serializers.SerializerMethodField()
    almacen_id = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = (
            'pk',
            'url',
            'orden',
            'articulo',
            'almacen',
            'articulo_id',
            'articulo_desc',
            'articulo_udm',
            'almacen_id',
            'cantidad_estimada',
            'cantidad_real',
        )

    def get_articulo_id(self, obj):

        try:
            return obj.articulo.id

        except:
            return 0

    def get_articulo_desc(self, obj):

        try:
            if (obj.articulo.clave is None or obj.articulo.clave == ""):
                clave = "-"
            else:
                clave = obj.articulo.clave
            descripcion = obj.articulo.descripcion
            return "(%s) %s" % (clave, descripcion)

        except:
            return ""

    def get_articulo_udm(self, obj):

        try:
            clave = obj.articulo.udm.clave
            descripcion = obj.articulo.udm.descripcion
            return "(%s) %s" % (clave, descripcion)

        except:
            return ""

    def get_almacen_id(self, obj):

        try:
            return obj.almacen.id

        except:
            return 0


# ----------------- MANO OBRA ----------------- #

class ManoObraSerializer(serializers.HyperlinkedModelSerializer):

    empleado_id = serializers.SerializerMethodField()
    empleado_desc = serializers.SerializerMethodField()

    class Meta:
        model = ManoObra
        fields = (
            'pk',
            'url',
            'orden',
            'empleado',
            'empleado_id',
            'empleado_desc',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'horas_estimadas',
            'horas_reales',
        )

    def get_empleado_id(self, obj):

        try:
            return obj.empleado.id

        except:
            return 0

    def get_empleado_desc(self, obj):

        try:
            full_name = obj.empleado.get_full_name()
            return full_name

        except:
            return ""


# ----------------- SERVICIO EXTERNO ----------------- #

class ServicioExternoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ServicioExterno
        fields = (
            'pk',
            'url',
            'orden',
            'clave_jde',
            'descripcion',
            'comentarios',
        )


# ------------- SOLICITUD DE COMPRA --------------------- #

class SolicitudCompraEncabezadoSerializer(serializers.HyperlinkedModelSerializer):

    created_by = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    solicitante = serializers.SerializerMethodField()

    class Meta:
        model = SolicitudCompraEncabezado
        fields = (
            'url',
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

    def get_estado(self, obj):
        try:
            return obj.get_estado_display()
        except:
            return ""

    def get_solicitante(self, obj):

        try:
            full_name = obj.solicitante.user.get_full_name()
            return full_name
        except:
            return ""

    def get_created_by(self, obj):
        try:
            full_name = obj.created_by.user.get_full_name()
            return full_name
        except:
            return ""


class SolicitudCompraDetalleSerializer(serializers.ModelSerializer):

    articulo_clave = serializers.SerializerMethodField()
    articulo_udm = serializers.SerializerMethodField()

    class Meta:
        model = SolicitudCompraDetalle
        fields = (
            'pk',
            'url',
            'cantidad',
            'articulo',
            'comentarios',
            'encabezado',
            'articulo_clave',
            'articulo_udm',
        )

    def get_articulo_clave(self, obj):

        try:
            if (obj.articulo.clave is None or obj.articulo.clave == ""):
                clave = "-"
            else:
                clave = obj.articulo.clave
            desc = obj.articulo.descripcion
            return "(%s) %s" % (clave, desc)
        except:
            return ""

    def get_articulo_udm(self, obj):

        try:

            clave = obj.articulo.udm.clave
            desc = obj.articulo.udm.descripcion
            return "(%s) %s" % (clave, desc)
        except:
            return ""
