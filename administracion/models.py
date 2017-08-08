# -*- coding: utf-8 -*-

# Librerias Django:
from __future__ import unicode_literals
from django.db import models

# Validadores:
from home.validators import valid_extension
from home.validators import validate_image

# Otros Modelos:
from django.contrib.auth.models import User

# Historia
from simple_history.models import HistoricalRecords


class Empresa(models.Model):

    clave = models.CharField(max_length=144, null=True)
    descripcion = models.CharField(max_length=144, null=True)
    logo = models.ImageField(
        upload_to='empresas/img/',
        blank=True,
        null=True,
        validators=[
            valid_extension,
            validate_image
        ]
    )
    created_by = models.ForeignKey(
        User,
        related_name='empresa_created_by',
        null=True,
        blank=True
    )
    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='empresa_updated_by',
        null=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.clave

    def __unicode__(self):
        return self.clave


class Contrato(models.Model):

    CONTRATO_ESTADO = (
        ('ACT', 'ACTIVO'),
        ('DES', 'DESHABILITADO'),
        ('REP', 'EN REPARACION'),
    )

    clave = models.CharField(max_length=144, null=True)
    nombre = models.CharField(max_length=144, null=True)
    descripcion = models.TextField(blank=True, null=True)
    cliente = models.CharField(max_length=144, null=True, blank=True)
    numero = models.CharField(max_length=144, null=True, blank=True)
    region = models.CharField(max_length=144, null=True, blank=True)

    estado = models.CharField(
        max_length=4,
        choices=CONTRATO_ESTADO,
        default="ACT",
        blank=True,
        null=True
    )
    logo = models.ImageField(
        upload_to='empresas/img/',
        blank=True,
        null=True,
        validators=[
            valid_extension,
            validate_image
        ]
    )
    # Campos de Auditoria:
    created_by = models.ForeignKey(
        User,
        related_name='contrato_created_by',
        null=True,
        blank=True
    )
    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='contrato_updated_by',
        null=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True
    )
    history = HistoricalRecords()

    def __str__(self):
        clave = self.clave
        desc = self.nombre
        return "{0} - {1}".format(clave, desc)

    def __unicode__(self):
        clave = self.clave
        desc = self.nombre
        return "{0} - {1}".format(clave, desc)


class Turno(models.Model):
    clave = models.CharField(max_length=10, null=True, unique=True)
    descripcion = models.CharField(max_length=144, null=True)
    hora_inicio = models.CharField(max_length=8, null=True)
    hora_fin = models.CharField(max_length=8, null=True)
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True
    )
    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='turno_updated_by',
        null=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True
    )
    history = HistoricalRecords()

    def __str__(self):
        clave = self.clave
        desc = self.descripcion
        return "{0} - {1}".format(clave, desc)

    def __unicode__(self):
        clave = self.clave
        desc = self.descripcion
        return "{0} - {1}".format(clave, desc)
