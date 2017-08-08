# -*- coding: utf-8 -*-

# Modelos:
from .models import Contrato
from .models import Empresa

# API REST:
from rest_framework import serializers


class ContratoSerializer(serializers.ModelSerializer):

    estado = serializers.SerializerMethodField()

    class Meta:
        model = Contrato
        fields = (
            'url',
            'pk',
            'clave',
            'nombre',
            'descripcion',
            'cliente',
            'numero',
            'region',
            'estado',
            'created_date',
            'created_by',
            'updated_date',
            'updated_by',
        )

    def get_estado(self, obj):
        try:
            return obj.get_estado_display()
        except:
            return ""


class EmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empresa
        fields = (
            'url',
            'pk',
            'clave',
            'descripcion',
            'logo',
        )
