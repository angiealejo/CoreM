# -*- coding: utf-8 -*-

# Librerias Django:
from __future__ import unicode_literals
from django.db import models

# Django Signals:
from django.db.models.signals import post_save
from django.dispatch import receiver

# Otros modelos:
from django.contrib.auth.models import User

# Validadores:
from home.validators import valid_extension
from home.validators import validate_image


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    puesto = models.CharField(
        max_length=144,
        null=True,
        blank=True
    )
    clave = models.CharField(
        max_length=144,
        null=True,
        blank=True
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)
    imagen = models.ImageField(
        upload_to='usuarios/img/',
        blank=True,
        null=True,
        validators=[
            valid_extension,
            validate_image
        ]
    )
    firma = models.ImageField(
        upload_to='usuarios/firma/',
        blank=True,
        null=True,
        validators=[
            valid_extension,
            validate_image
        ]
    )
    costo = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0, blank=True, null=True
    )
    comentarios = models.TextField(blank=True)

    def __unicode__(self):
        nombre_completo = self.user.get_full_name()
        return nombre_completo


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
