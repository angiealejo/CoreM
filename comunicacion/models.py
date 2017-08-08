# -*- coding: utf-8 -*-

# Librerias Django:
from __future__ import unicode_literals
from django.db import models

# Otros modelos:
from django.contrib.auth.models import User


class Mensaje(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        null=True,
        blank=True
    )

    def __str__(self):
        value = "%s : %s " % (self.usuario, self.created_date)
        return value

    def __unicode__(self):
        value = "%s : %s " % (self.usuario, self.created_date)
        return value

