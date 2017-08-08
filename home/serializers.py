# -*- coding: utf-8 -*-

# API REST:
from rest_framework import serializers
# Modelos:
from .models import AnexoTexto
from .models import AnexoArchivo
from .models import AnexoImagen


class AnexoTextoSerializer(serializers.HyperlinkedModelSerializer):

    equipo = serializers.SerializerMethodField()
    articulo = serializers.SerializerMethodField()

    class Meta:
        model = AnexoTexto
        fields = (
            'url',
            'pk',
            'equipo',
            'articulo',
            'texto',
        )

    def get_equipo(self, obj):
        try:
            return obj.equipo.tag
        except:
            return ""

    def get_articulo(self, obj):
        try:
            return obj.articulo.clave
        except:
            return ""


class AnexoArchivoSerializer(serializers.HyperlinkedModelSerializer):

    equipo = serializers.SerializerMethodField()
    articulo = serializers.SerializerMethodField()

    class Meta:
        model = AnexoArchivo
        fields = (
            'url',
            'pk',
            'equipo',
            'articulo',
            'archivo',
            'descripcion',
        )

    def get_equipo(self, obj):
        try:
            return obj.equipo.tag
        except:
            return ""

    def get_articulo(self, obj):
        try:
            return obj.articulo.clave
        except:
            return ""


class AnexoImagenSerializer(serializers.HyperlinkedModelSerializer):

    equipo = serializers.SerializerMethodField()
    articulo = serializers.SerializerMethodField()

    class Meta:
        model = AnexoImagen
        fields = (
            'url',
            'pk',
            'equipo',
            'articulo',
            'ruta',
            'descripcion',
        )

    def get_equipo(self, obj):
        try:
            return obj.equipo.tag
        except:
            return ""

    def get_articulo(self, obj):
        try:
            return obj.articulo.clave
        except:
            return ""
