# -*- coding: utf-8 -*-

# API REST:
from rest_framework import serializers

# Modelos:
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk',
            'url',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'is_active',

        )

    def get_full_name(self, obj):

        try:
            return obj.get_full_name()

        except:
            return 0


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'pk',
            'url',
            'username',
            'puesto',
            'clave',
            'fecha_nacimiento',
            'imagen',
            'firma',
            'costo',
            'comentarios',
        )

    def get_username(self, obj):
        try:
            return obj.user.username
        except:
            return ""


class ProfileExcelSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'pk',
            'url',
            'username',
            'full_name',
            'puesto',
            'clave',
            'email',
            'fecha_nacimiento',
            'imagen',
            'costo',
            'comentarios',
        )

    def get_username(self, obj):
        try:
            return obj.user.username
        except:
            return ""

    def get_full_name(self, obj):

        try:
            return obj.user.get_full_name()

        except:
            return 0

    def get_email(self, obj):

        try:
            return obj.user.email

        except:
            return 0
