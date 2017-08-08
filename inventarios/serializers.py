# -*- coding: utf-8 -*-

# API REST:
from rest_framework import serializers

# Modelos:
from .models import Almacen
from .models import Stock
from .models import Articulo
from .models import MovimientoCabecera
from .models import MovimientoDetalle
from .models import UdmArticulo
from .models import SeccionAlmacen


class Reporte(object):
    def __init__(self, _articulo, _almacen, _stock, _necesidad, _pedido):
        self.articulo = _articulo
        self.almacen = _almacen
        self.stock = _stock
        self.necesidad = _necesidad
        self.pedido = _pedido


class ReporteSerializer(serializers.Serializer):
    articulo = serializers.CharField(max_length=128, required=False)
    almacen = serializers.CharField(max_length=128)
    stock = serializers.CharField(max_length=128, required=False)
    necesidad = serializers.CharField(max_length=10, required=False)
    pedido = serializers.CharField(max_length=254, required=False)

    def create(self, validated_data):
        return Reporte(**validated_data)
# ----------------- ALMACEN ----------------- #


class AlmacenSerializer(serializers.ModelSerializer):

    estado = serializers.SerializerMethodField()

    class Meta:
        model = Almacen
        fields = (
            'url',
            'pk',
            'clave',
            'descripcion',
            'estado',
        )

    def get_estado(self, obj):
        try:
            return obj.get_estado_display()
        except Exception:
            return ""


class SeccionAlmacenSerializer(serializers.ModelSerializer):

    class Meta:
        model = SeccionAlmacen
        fields = (
            'pk',
            'url',
            'clave',
            'descripcion'
        )

# ----------------- STOCK ----------------- #


class StockSerializer(serializers.ModelSerializer):

    almacen = serializers.SerializerMethodField()
    articulo = serializers.SerializerMethodField()
    articulo_clave = serializers.SerializerMethodField()
    articulo_stock_seg = serializers.SerializerMethodField()
    udm = serializers.SerializerMethodField()
    art_marca = serializers.SerializerMethodField()
    art_modelo = serializers.SerializerMethodField()
    art_numero_parte = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = (
            'url',
            'pk',
            'almacen',
            'articulo',
            'articulo_clave',
            'articulo_stock_seg',
            'cantidad',
            'udm',
            'art_marca',
            'art_modelo',
            'art_numero_parte',
        )

    def get_almacen(self, obj):

        try:
            descripcion = obj.almacen.descripcion
            return "%s" % (descripcion)

        except Exception:
            return ""

    def get_articulo(self, obj):

        try:
            if (obj.articulo.clave is None or obj.articulo.clave == ""):
                clave = "-"
            else:
                clave = obj.articulo.clave
            descripcion = obj.articulo.descripcion
            return "(%s) %s" % (clave, descripcion)

        except Exception:
            return ""

    def get_articulo_stock_seg(self, obj):
        try:
            return obj.articulo.stock_seguridad
        except Exception:
            return ""

    def get_articulo_clave(self, obj):
        try:
            if obj.articulo.clave is not None:
                return obj.articulo.clave
            else:
                return ""
        except Exception:
            return ""

    def get_udm(self, obj):

        try:
            clave = obj.articulo.udm.clave
            descripcion = obj.articulo.udm.descripcion
            return "(%s) %s" % (clave, descripcion)
        except Exception:
            return ""

    def get_art_marca(self, obj):
        try:
            if (obj.articulo.marca is None):
                marca = ""
            else:
                marca = obj.articulo.marca
            return marca
        except Exception:
            return ""

    def get_art_modelo(self, obj):
        try:
            if (obj.articulo.modelo is None):
                modelo = ""
            else:
                modelo = obj.articulo.modelo
            return modelo
        except Exception:
            return ""

    def get_art_numero_parte(self, obj):
        try:
            if (obj.articulo.numero_parte is None):
                numero_parte = ""
            else:
                numero_parte = obj.articulo.numero_parte
            return numero_parte
        except Exception:
            return ""


# ----------------- UDM ODOMETRO ----------------- #

class UdmArticuloSerializer(serializers.ModelSerializer):

    class Meta:
        model = UdmArticulo
        fields = (
            'pk',
            'url',
            'clave',
            'descripcion'
        )


# ----------------- ARTICULO ----------------- #

class ArticuloSerializer(serializers.HyperlinkedModelSerializer):

    tipo = serializers.SerializerMethodField()
    udm = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    informacion = serializers.SerializerMethodField()

    class Meta:
        model = Articulo
        fields = (
            'url',
            'pk',
            'clave',
            'descripcion',
            'tipo',
            'estado',
            'marca',
            'modelo',
            'numero_parte',
            'udm',
            'observaciones',
            'url',
            'stock_seguridad',
            'stock_minimo',
            'stock_maximo',
            'clave_jde',
            'informacion',
        )

    def get_tipo(self, obj):
        try:
            return obj.get_tipo_display()
        except Exception:
            return ""

    def get_udm(self, obj):

        try:
            return obj.udm.descripcion

        except Exception:
            return ""

    def get_informacion(self, obj):

        try:
            if obj.clave is None or obj.clave == "":
                clave = "-"
            else:
                clave = obj.clave
            udm_descripcion = obj.udm.descripcion
            descripcion = obj.descripcion
            estado = obj.get_estado_display()
            if obj.get_estado_display() == "DESHABILITADO":

                return "(%s) %s (%s) - %s" % (
                    clave,
                    descripcion,
                    udm_descripcion,
                    estado
                )
            else:
                return "(%s) %s (%s)" % (
                    clave,
                    descripcion,
                    udm_descripcion,
                )

        except Exception:
            return ""

    def get_estado(self, obj):
        try:
            return obj.get_estado_display()
        except Exception:
            return ""


# ----------------- ENTRADA ----------------- #

class MovimientoCabeceraSerializer(serializers.HyperlinkedModelSerializer):
    estado = serializers.SerializerMethodField()
    almacen_origen = serializers.SerializerMethodField()
    almacen_destino = serializers.SerializerMethodField()
    persona_recibe = serializers.SerializerMethodField()
    persona_entrega = serializers.SerializerMethodField()
    clasificacion = serializers.SerializerMethodField()
    orden_trabajo = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    class Meta:
        model = MovimientoCabecera
        fields = (
            'pk',
            'url',
            'fecha',
            'descripcion',
            'almacen_origen',
            'almacen_destino',
            'persona_recibe',
            'persona_entrega',
            'tipo',
            'estado',
            'proveedor',
            'clasificacion',
            'orden_trabajo',
            'created_by',
            'updated_by'
        )

    def get_estado(self, obj):

        try:
            return obj.get_estado_display()
        except Exception:
            return ""

    def get_almacen_origen(self, obj):

        try:
            descripcion = obj.almacen_origen.descripcion
            return "%s" % (descripcion)
        except Exception:
            return ""

    def get_almacen_destino(self, obj):

        try:
            descripcion = obj.almacen_destino.descripcion
            return "%s" % (descripcion)
        except Exception:
            return ""

    def get_persona_recibe(self, obj):
        try:
            full_name = obj.persona_recibe.user.get_full_name()

            return full_name
        except Exception:
            return ""

    def get_persona_entrega(self, obj):
        try:
            full_name = obj.persona_entrega.user.get_full_name()

            return full_name
        except Exception:
            return ""

    def get_clasificacion(self, obj):
        try:
            return obj.get_clasificacion_display()
        except Exception:
            return ""

    def get_orden_trabajo(self, obj):
        try:
            return "(%s) %s" % (obj.orden_trabajo.pk, obj.orden_trabajo.descripcion)
        except Exception:
            return ""

    def get_created_by(self, obj):
        try:
            full_name = obj.created_by.user.get_full_name()

            return full_name
        except Exception:
            return ""

    def get_updated_by(self, obj):
        try:
            return "(%s) %s" % (obj.updated_by.user.username, obj.updated_by.user.get_full_name())
        except Exception:
            return ""


class MovimientoDetalleSerializer(serializers.ModelSerializer):

    articulo_clave = serializers.SerializerMethodField()
    articulo_udm = serializers.SerializerMethodField()

    class Meta:
        model = MovimientoDetalle
        fields = (
            'pk',
            'url',
            'cantidad',
            'articulo',
            'cabecera',
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
        except Exception:
            return ""

    def get_articulo_udm(self, obj):

        try:
            clave = obj.articulo.udm.clave
            desc = obj.articulo.udm.descripcion
            return "(%s) %s" % (clave, desc)
        except Exception:
            return ""


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    articulo_detalle = serializers.SerializerMethodField()
    articulo_udm = serializers.SerializerMethodField()
    cabecera_descripcion = serializers.SerializerMethodField()
    cabecera_tipo = serializers.SerializerMethodField()
    cabecera_clasificacion = serializers.SerializerMethodField()
    cabecera_almacen_origen = serializers.SerializerMethodField()
    cabecera_almacen_destino = serializers.SerializerMethodField()
    cabecera_persona_recibe = serializers.SerializerMethodField()
    cabecera_persona_entrega = serializers.SerializerMethodField()
    cabecera_fecha = serializers.SerializerMethodField()
    cabecera_proveedor = serializers.SerializerMethodField()
    cabecera_estado = serializers.SerializerMethodField()
    cabecera_orden_trabajo = serializers.SerializerMethodField()
    cabecera_created_by = serializers.SerializerMethodField()

    class Meta:
        model = MovimientoDetalle
        fields = (
            'pk',
            'articulo',
            'articulo_detalle',
            'cantidad',
            'articulo_udm',
            'cabecera',
            'cabecera_descripcion',
            'cabecera_tipo',
            'cabecera_clasificacion',
            'cabecera_almacen_origen',
            'cabecera_almacen_destino',
            'cabecera_persona_recibe',
            'cabecera_persona_entrega',
            'cabecera_fecha',
            'cabecera_proveedor',
            'cabecera_estado',
            'cabecera_orden_trabajo',
            'cabecera_created_by',

        )

    def get_articulo_udm(self, obj):
        try:
            return str(obj.articulo.udm)
        except Exception:
            return ""

    def get_articulo_detalle(self, obj):
        try:
            if obj.articulo.clave is None or obj.articulo.clave == "":
                clave = "-"
            else:
                clave = obj.articulo.clave
            descripcion = obj.articulo.descripcion
            return "(%s) %s" % (clave, descripcion)
        except Exception:
            return ""

    def get_cabecera_descripcion(self, obj):
        try:
            return obj.cabecera.descripcion
        except Exception:
            return ""

    def get_cabecera_tipo(self, obj):
        try:
            return obj.cabecera.get_tipo_display()
        except Exception:
            return ""

    def get_cabecera_clasificacion(self, obj):
        try:
            return obj.cabecera.get_clasificacion_display()
        except Exception:
            return ""

    def get_cabecera_almacen_origen(self, obj):
        try:
            descripcion = obj.cabecera.almacen_origen.descripcion
            return "%s" % (descripcion)
        except Exception:
            return ""

    def get_cabecera_almacen_destino(self, obj):
        try:
            descripcion = obj.cabecera.almacen_destino.descripcion
            return "%s" % (descripcion)
        except Exception:
            return ""

    def get_cabecera_persona_recibe(self, obj):
        try:
            full_name = obj.cabecera.persona_recibe.user.get_full_name()
            return full_name
        except Exception:
            return ""

    def get_cabecera_persona_entrega(self, obj):
        try:
            full_name = obj.cabecera.persona_entrega.user.get_full_name()
            return full_name
        except Exception:
            return ""

    def get_cabecera_fecha(self, obj):
        try:
            return obj.cabecera.fecha
        except Exception:
            return ""

    def get_cabecera_proveedor(self, obj):
        try:
            proveedor = obj.cabecera.proveedor
            if proveedor is not None:
                return "%s" % (proveedor)
            else:
                return ""
        except Exception:
            return ""

    def get_cabecera_estado(self, obj):
        try:
            return obj.cabecera.get_estado_display()
        except Exception:
            return ""

    def get_cabecera_orden_trabajo(self, obj):
        try:
            equipo = obj.cabecera.orden_trabajo.equipo
            descripcion = obj.cabecera.orden_trabajo.descripcion
            return "(%s) %s" % (equipo, descripcion)
        except Exception:
            return ""

    def get_cabecera_created_by(self, obj):
        try:
            full_name = obj.cabecera.created_by.user.get_full_name()
            return full_name
        except Exception:
            return ""
