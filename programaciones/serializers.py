# -*- coding: utf-8 -*-

# API REST:
from rest_framework import serializers

# Modelos:
from .models import Programa


class ProgramaSerializer(serializers.ModelSerializer):

    equipo = serializers.SerializerMethodField()

    class Meta:
        model = Programa
        fields = (
            'equipo',
            'descripcion',
            'periodicidad',
            'frecuencia',
            'fecha',
            'esta_activo',
            'observaciones',
        )

    def get_equipo(self, obj):

        try:
            tag = obj.equipo.tag
            desc = obj.equipo.descripcion
            return "(%s) %s" % (tag, desc)
        except:
            return ""
