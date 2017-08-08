# -*- coding: utf-8 -*-

# Librerias Django:
from __future__ import unicode_literals
from django.db import models


# Otros Modelos:
from activos.models import Equipo
# from activos.models import Odometro


class Programa(models.Model):

    PERIODICIDAD = (
        ('DIA', 'DIA'),
        ('SEM', 'SEMANAL'),
        ('MEN', 'MES'),
        ('ANI', 'AÑO'),
    )

    equipo = models.ForeignKey(Equipo)
    descripcion = models.CharField(max_length=144, null=True)
    periodicidad = models.CharField(
        max_length=4,
        choices=PERIODICIDAD,
    )
    frecuencia = models.IntegerField()
    fecha = models.DateField(null=True)
    esta_activo = models.BooleanField(default=False)
    observaciones = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{0} : {1}".format(self.equipo, self.descripcion)
