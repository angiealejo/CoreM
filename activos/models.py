# -*- coding: utf-8 -*-

# Librerias Django:
from __future__ import unicode_literals
from django.db import models

# Validadores:
from home.validators import valid_extension
from home.validators import validate_image

# Historia
from simple_history.models import HistoricalRecords

# Otros Modelos:
from seguridad.models import Profile
from administracion.models import Contrato


class Ubicacion(models.Model):
    clave = models.CharField(max_length=144, null=True)
    descripcion = models.CharField(max_length=144, null=True)
    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
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
        return "({}) {}".format(
            clave,
            desc
        )

    def __unicode__(self):
        clave = self.clave
        desc = self.descripcion
        return "({}) {}".format(
            clave,
            desc
        )

    class Meta:
        verbose_name_plural = "Ubicaciones"


class TipoEquipo(models.Model):
    clave = models.CharField(max_length=144, null=True, unique=True)
    descripcion = models.CharField(max_length=144, null=True)

    # Campos de Auditoria:
    created_by = models.ForeignKey(
        Profile,
        related_name='tipoequipo_created_by',
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
        Profile,
        related_name='tipoequipo_updated_by',
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
        return "({0}) {1}".format(self.clave, self.descripcion)

    def __unicode__(self):
        return "({0}) {1}".format(self.clave, self.descripcion)


class Equipo(models.Model):

    EQUIPO_ESTADO = (
        # esta operando
        ('ACT', 'TRABAJANDO'),
        # No esta operando y no se esta listo para operar
        ('NOD', 'NO DISPONIBLE'),
        # No esta operando y esta listo para operar
        ('DIS', 'DISPONIBLE'),
        ('REP', 'EN REPARACION'),
        ('MTTO', 'EN MANTENIMIENTO'),
        ('V', 'VACIO'),
    )

    tag = models.CharField(max_length=144, null=True)
    descripcion = models.CharField(max_length=144, null=True)
    serie = models.CharField(max_length=144, null=True, blank=True)
    especialidad = models.CharField(max_length=144, null=True, blank=True)
    estado = models.CharField(
        max_length=4,
        choices=EQUIPO_ESTADO
    )
    tipo = models.ForeignKey(
        TipoEquipo,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    contrato = models.ForeignKey(
        Contrato,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    padre = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    sistema = models.CharField(max_length=144, null=True, blank=True)
    ubicacion = models.ForeignKey(
        Ubicacion,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    imagen = models.ImageField(
        upload_to='equipos/img',
        blank=True,
        validators=[
            valid_extension,
            validate_image
        ]
    )
    cliente = models.CharField(max_length=144, null=True, blank=True)
    responsable = models.ForeignKey(Profile, null=True, blank=True)
    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
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

        tag = self.tag
        desc = self.descripcion
        estado = self.get_estado_display()
        if estado != "ACTIVO":

            return "(%s) %s - (%s)" % (tag, desc, estado)
        else:
            return "(%s) %s" % (tag, desc)

    def __unicode__(self):

        tag = self.tag
        desc = self.descripcion
        estado = self.get_estado_display()
        if estado != "ACTIVO":

            return "(%s) %s - (%s)" % (tag, desc, estado)
        else:
            return "(%s) %s" % (tag, desc)


class Asignacion(models.Model):
    equipo = models.ForeignKey(Equipo)
    ubicacion = models.ForeignKey(Ubicacion)
    fecha = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
    )
    history = HistoricalRecords()

    def __str__(self):
        return "({0}) {1}".format(self.equipo, self.ubicacion)

    def __unicode__(self):
        return "({0}) {1}".format(self.equipo, self.ubicacion)

    class Meta:
        unique_together = (('equipo', 'ubicacion'),)
        verbose_name_plural = "Asignaciones"


class UdmOdometro(models.Model):
    clave = models.CharField(max_length=144, unique=True)
    descripcion = models.CharField(max_length=144, null=True)
    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
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
        return "({}) {}".format(
            clave,
            desc
        )

    def __unicode__(self):
        clave = self.clave
        desc = self.descripcion
        return "({}) {}".format(
            clave,
            desc
        )


class TipoOdometro(models.Model):
    clave = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=144)
    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
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

    def __unicode__(self):

        return "({0}) - {1}".format(self.clave, self.descripcion)

    def __str__(self):
        return "({0}) - {1}".format(self.clave, self.descripcion)


class Odometro(models.Model):

    ACUMULADO = (
        ('ULT', 'ULTIMO VALOR'),
        ('SUM', 'SUMA DE VALORES')
    )
    CLASIFICACION = (
        ('NUM', 'NUMÉRICO'),
        ('TEX', 'TEXTO'),
        ('OPC', 'OPCIONAL')

    )
    clave = models.CharField(max_length=144)
    descripcion = models.CharField(max_length=144, null=True)
    udm = models.ForeignKey(UdmOdometro, null=True, on_delete=models.PROTECT)
    esta_activo = models.BooleanField(default=True)
    acumulado = models.CharField(
        max_length=4,
        choices=ACUMULADO,
        default="SUM"
    )
    clasificacion = models.CharField(
        max_length=4,
        choices=CLASIFICACION,
        default="NUM"
    )
    tipo = models.ForeignKey(TipoOdometro, null=True, on_delete=models.PROTECT)
    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
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
        descripcion = self.descripcion
        return "({0}) {1}".format(clave, descripcion)

    def __unicode__(self):
        clave = self.clave
        descripcion = self.descripcion
        return "({0}) {1}".format(clave, descripcion)


class Medicion(models.Model):
    odometro = models.ForeignKey(Odometro, null=True, blank=True, on_delete=models.PROTECT)
    equipo = models.ForeignKey(Equipo, null=True, blank=True, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    lectura = models.DecimalField(max_digits=20, decimal_places=6, default=0.0)
    observaciones = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        null=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="medicion_created_by"
    )
    updated_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True
    )
    history = HistoricalRecords()

    @property
    def _history_lecturap(self):
        return self.lectura

    @_history_lecturap.setter
    def _history_lecturap(self, value):
        self.lectura = value

    def __str__(self):
        return "({0} - {1}) {2}".format(self.odometro.description, self.equipo, self.fecha)

    def __unicode__(self):
        return "({0} - {1}) {2}".format(self.odometro.descripcion, self.equipo.descripcion, self.fecha)

    class Meta:
        verbose_name_plural = "Mediciones"


# class Sistema(models.Model):
#     clave = models.CharField(max_length=144, null=True)
#     descripcion = models.CharField(max_length=144, null=True)

#     # Campos de Auditoria:
#     created_by = models.ForeignKey(
#         User,
#         related_name='contrato_created_by',
#         null=True,
#         blank=True
#     )
#     created_date = models.DateTimeField(
#         auto_now=False,
#         auto_now_add=True,
#         null=True,
#         blank=True
#     )
#     updated_by = models.ForeignKey(
#         User,
#         related_name='contrato_updated_by',
#         null=True,
#         blank=True
#     )
#     updated_date = models.DateTimeField(
#         auto_now=True,
#         auto_now_add=False,
#         null=True,
#         blank=True
#     )
#     history = HistoricalRecords()


#     def __str__(self):
#         return self.clave.encode('utf-8')
