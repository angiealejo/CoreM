# -*- coding: utf-8 -*-

# API REST:
from rest_framework import serializers

# Modelos:
from .models import Mensaje


# ----------------- ORDEN DE TRABAJO ----------------- #
class MensajeSerializer(serializers.HyperlinkedModelSerializer):

    usuario_id = serializers.SerializerMethodField()
    usuario_nombre = serializers.SerializerMethodField()
    usuario_img = serializers.SerializerMethodField()

    class Meta:
        model = Mensaje
        fields = (
            'url',
            'pk',
            'usuario_id',
            'usuario_nombre',
            'usuario_img',
            'usuario',
            'texto',
            'created_date',
        )

    def get_usuario_id(self, obj):

        try:
            return obj.usuario.id
        except:
            return ""

    def get_usuario_nombre(self, obj):

        try:
            return obj.usuario.get_full_name()
        except:
            return ""

    def get_usuario_img(self, obj):

        try:
            return obj.usuario.profile.imagen.url
        except:
            return ""
