# -*- coding: utf-8 -*-

# Librerias Python:
import sys
import json

# API REST:
from rest_framework import serializers

# Modelos:
from .models import Equipo
from .models import Ubicacion
from .models import Odometro
from .models import Medicion
from .models import UdmOdometro
from .models import TipoOdometro
from .models import TipoEquipo

# ----------------- EQUIPO ----------------- #


class TipoEquipoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoEquipo
        fields = (
            'pk',
            'url',
            'clave',
            'descripcion'
        )


class EquipoSerializer(serializers.HyperlinkedModelSerializer):

    padre = serializers.SerializerMethodField()
    ubicacion = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    tipo = serializers.SerializerMethodField()

    class Meta:
        model = Equipo
        fields = (
            'url',
            'pk',
            'tag',
            'descripcion',
            'serie',
            'especialidad',
            'estado',
            'tipo',
            'padre',
            'sistema',
            'ubicacion',
        )

    def get_padre(self, obj):

        try:
            tag = obj.padre.tag
            descripcion = obj.padre.descripcion
            return "(%s) %s" % (tag, descripcion)

        except:
            return ""

    def get_ubicacion(self, obj):

        try:
            clave = obj.ubicacion.clave
            descripcion = obj.ubicacion.descripcion
            return "(%s) %s" % (clave, descripcion)
        except:
            return ""

    def get_estado(self, obj):
        try:
            return obj.get_estado_display()
        except:
            return ""

    def get_tipo(self, obj):
        try:
            cv = obj.tipo.clave
            desc = obj.tipo.descripcion
            return "(%s) %s" % (cv, desc)
        except:
            return ""


class EquipoTreeSerilizado(object):

    def __init__(self):
        self.lista = []

    def get_Descendencia(self, _hijos, _nodo_padre):

        lista_desendencia = []

        for hijo in _hijos:
            span = ""
            if hijo.estado == "ACT":
                span = "<span class='label label-success'>"
            if hijo.estado == "NOD":
                span = "<span class='label label-default'>"
            if hijo.estado == "DIS":
                span = "<span class='label label-disponible'>"
            if hijo.estado == "REP":
                span = "<span class='label label-warning'>"

            nodo = {}

            nodo["text"] = "%s : %s - %s %s </span>" % (
                hijo.tag,
                hijo.descripcion,
                span,
                hijo.get_estado_display(),
            )
            nodo["clave"] = hijo.id
            nietos = Equipo.objects.filter(padre=hijo)

            if len(nietos):
                nodo["nodes"] = self.get_Descendencia(nietos, nodo)

            lista_desendencia.append(nodo)

        return lista_desendencia

    def get_Json(self, _daddies):

        sys.setrecursionlimit(1500)

        self.lista = []

        for daddy in _daddies:

            nodo = {}

            nodo["icon"] = "fa fa-sitemap"
            hijos = Equipo.objects.filter(padre=daddy)

            if len(hijos):

                nodo["text"] = "Sub-Equipos:"
                nodo["nodes"] = self.get_Descendencia(hijos, nodo)
                nodo["backColor"] = "#307AAE"
                nodo["color"] = "#FFFFFF"
                nodo["clave"] = daddy.id
            else:

                nodo["text"] = "Sin Sub-Equipos"
                nodo["backColor"] = "#F2F2F2"
                nodo["color"] = "#000000"
                nodo["clave"] = daddy.id

            self.lista.append(nodo)

        lista_json = json.dumps(self.lista)

        return lista_json


class EquipoTreeSerilizado2(object):

    def __init__(self):
        self.lista = []

    def get_Descendencia(self, _hijos, _nodo_padre):

        lista_desendencia = []

        for hijo in _hijos:

            nodo = {}

            nodo["text"] = "%s : %s" % (hijo.tag, hijo.descripcion)
            nodo["clave"] = hijo.id

            nietos = Equipo.objects.filter(padre=hijo)

            if len(nietos):
                nodo["nodes"] = self.get_Descendencia(nietos, nodo)

            lista_desendencia.append(nodo)

        return lista_desendencia

    def get_Json(self, _daddies):

        sys.setrecursionlimit(1500)

        self.lista = []

        for daddy in _daddies:

            nodo = {}
            # nodo["text"] = daddy.descripcion
            # nodo["href"] = "#{}".format(daddy.id)
            # nodo["tag"] = ['0']
            nodo["icon"] = "fa fa-sitemap"
            # nodo["id"] = daddy.id
            hijos = Equipo.objects.filter(padre=daddy)

            if len(hijos):

                nodo["text"] = "Sub-Equipos de: " + daddy.tag + ": " + daddy.descripcion
                nodo["nodes"] = self.get_Descendencia(hijos, nodo)
                nodo["backColor"] = "#307AAE"
                nodo["color"] = "#FFFFFF"
                nodo["clave"] = daddy.id
            else:

                nodo["text"] = daddy.tag + ": " + daddy.descripcion
                nodo["backColor"] = "#F2F2F2"
                nodo["color"] = "#000000"
                nodo["clave"] = daddy.id

            self.lista.append(nodo)

        lista_json = json.dumps(self.lista)

        return lista_json

# ----------------- UBICACION ----------------- #


class UbicacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ubicacion
        fields = (
            'pk',
            'url',
            'clave',
            'descripcion'
        )


# ----------------- UDM ODOMETRO ----------------- #

class UdmOdometroSerializer(serializers.ModelSerializer):

    class Meta:
        model = UdmOdometro
        fields = (
            'pk',
            'url',
            'clave',
            'descripcion'
        )


# ----------------- ODOMETRO ------------------ #

class OdometroSerializer(serializers.ModelSerializer):

    udm = serializers.SerializerMethodField()
    tipo_odo = serializers.SerializerMethodField()
    acumulado = serializers.SerializerMethodField()
    clasificacion = serializers.SerializerMethodField()

    class Meta:
        model = Odometro
        fields = (
            'pk',
            'url',
            'clave',
            'descripcion',
            'udm',
            'esta_activo',
            'acumulado',
            'tipo',
            'tipo_odo',
            'clasificacion',
        )

    def get_udm(self, obj):

        try:
            clave = obj.udm.clave
            descripcion = obj.udm.descripcion
            return "(%s) %s" % (clave, descripcion)
        except Exception:
            return ""

    def get_acumulado(self, obj):
        try:
            return "%s" % (obj.get_acumulado_display())
        except Exception:
            return ""

    def get_tipo_odo(self, obj):

        try:
            clave = obj.tipo.clave
            descripcion = obj.tipo.descripcion
            return "(%s) %s" % (clave, descripcion)
        except Exception:
            return ""

    def get_clasificacion(self, obj):
        try:
            return "%s" % (obj.get_clasificacion_display())
        except Exception:
            return ""

# ----------------- MEDICION ------------------ #

class MedicionSerializer(serializers.ModelSerializer):

    creado_por = serializers.SerializerMethodField()
    modificado_por = serializers.SerializerMethodField()

    class Meta:
        model = Medicion
        fields = (
            'pk',
            'url',
            'equipo',
            'odometro',
            'fecha',
            'lectura',
            'observaciones',
            'created_by',
            'updated_by',
            'creado_por',
            'modificado_por',
        )

    def get_creado_por(self, obj):

        try:
            nombre = obj.created_by.user.get_full_name()
            return nombre
        except Exception:
            return ""

    def get_modificado_por(self, obj):

        try:
            nombre = obj.updated_by.user.get_full_name()
            return nombre
        except Exception:
            return ""


# ----------------- TIPO ODOMETRO ----------------- #

class TipoOdometroSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoOdometro
        fields = (
            'pk',
            'url',
            'clave',
            'descripcion'
        )


# ----------------- MEDICION HISTORY --------------- #

class History(serializers.ModelSerializer):
    def __init__(self, model, fields='__all__', *args, **kwargs):
        self.Meta.model = model
        self.Meta.fields = fields
        super().__init__()

    class Meta:
        pass


class MedicionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicion
        fields = '__all__'

    history = serializers.SerializerMethodField()

    def get_history(self, obj):
        try:
            h = obj.history.all()
            return h
        except Exception:
            return ""

        # model = obj.history.__dict__['model']
        # fields = ['history_id', ]
        # serializer = History(model, obj.history.all().order_by('history_date'), fields=fields)
        # serializer.is_valid()
        # return serializer.data

# class MedicionHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Medicion
#         fields = '__all__'
