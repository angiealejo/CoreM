# -*- coding: utf-8 -*-

# Librerias Django:
from __future__ import unicode_literals
from django.db import models

# Validadores:
from home.validators import valid_extension
from home.validators import validate_image

# Utilidades_
from .utilities import get_FilePath
from .utilities import get_ImagePath

# Modelos
from activos.models import Equipo
from inventarios.models import Articulo
from trabajos.models import OrdenTrabajo


class AnexoArchivo(models.Model):
    equipo = models.ForeignKey(Equipo, null=True, blank=True)
    articulo = models.ForeignKey(Articulo, null=True, blank=True)
    orden_trabajo = models.ForeignKey(OrdenTrabajo, null=True, blank=True)
    archivo = models.FileField(upload_to=get_FilePath)
    descripcion = models.CharField(max_length=255, null=True, blank=True)


class AnexoTexto(models.Model):
    equipo = models.ForeignKey(Equipo, null=True, blank=True)
    articulo = models.ForeignKey(Articulo, null=True, blank=True)
    orden_trabajo = models.ForeignKey(OrdenTrabajo, null=True, blank=True)
    titulo = models.CharField(max_length=60)
    texto = models.CharField(max_length=255, null=True, blank=True)


class AnexoImagen(models.Model):
    equipo = models.ForeignKey(Equipo, null=True, blank=True)
    articulo = models.ForeignKey(Articulo, null=True, blank=True)
    orden_trabajo = models.ForeignKey(OrdenTrabajo, null=True, blank=True)
    ruta = models.ImageField(
        upload_to=get_ImagePath,
        validators=[
            valid_extension,
            validate_image
        ])
    descripcion = models.CharField(max_length=255, null=True)
