# -*- coding: utf-8 -*-

# Librerias Django:
from __future__ import unicode_literals
from django.db import models

# Otros Modelos:
from django.contrib.auth.models import User
from seguridad.models import Profile
from activos.models import Equipo
from inventarios.models import Articulo
from inventarios.models import Almacen
from inventarios.models import MovimientoDetalle

# Validadores:
from home.validators import valid_extension
from home.validators import validate_image

# Historia
from simple_history.models import HistoricalRecords

# Signals
from django.db.models.signals import post_save
from django.dispatch import receiver


SOLICITUD_COMPRA_ESTADO = (
    ('CAP', 'CAPTURA'),
    ('CER', 'CERRADO'),
)


class OrdenTrabajo(models.Model):

    ORDEN_TIPO = (
        ('PREVE', 'PREVENTIVA'),
        ('PREDI', 'PREDICTIVA'),
        ('CORRE', 'CORRECTIVA'),
        ('INST', 'INSTALACIÓN'),
    )

    ORDEN_ESTADO = (
        ('CAP', 'ABIERTA'),
        ('TER', 'TERMINADA'),
        ('CER', 'CERRADA'),
        ('CAN', 'CANCELADA'),
    )
    ORDEN_ESPECIALIDAD = (
        ('COM', 'COMUNICACION'),
        ('ELEC', 'ELECTRICO'),
        ('INST', 'INSTRUMENTOS'),
        ('MEC', 'MECANICO'),
        ('SEG', 'SEGURIDAD'),
        ('CRT', 'CONTROL'),
    )

    equipo = models.ForeignKey(Equipo)
    descripcion = models.CharField(max_length=144, null=True)
    especialidad = models.CharField(
        max_length=6,
        choices=ORDEN_ESPECIALIDAD,
        blank=True,
        default="ELEC"
    )
    codigo_reporte = models.CharField(max_length=30, blank=True)
    tipo = models.CharField(
        max_length=6,
        choices=ORDEN_TIPO,
        default="COM",
    )

    estado = models.CharField(
        max_length=5,
        choices=ORDEN_ESTADO,
        default="CAP",
    )

    solicitante = models.ForeignKey(
        Profile,
        related_name='orden_solicitante',
        null=True,
        blank=True
    )
    responsable = models.ForeignKey(
        Profile,
        related_name='orden_responsable',
        null=True,
        blank=True
    )
    fecha_estimada_inicio = models.DateTimeField(null=True, blank=True)
    fecha_estimada_fin = models.DateTimeField(null=True, blank=True)
    fecha_real_inicio = models.DateTimeField(null=True, blank=True)
    permiso = models.CharField(max_length=144, null=True, blank=True)
    fecha_real_fin = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    motivo_cancelacion = models.TextField(null=True, blank=True)
    es_template = models.BooleanField(default=False)

    
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
        return "({0}) {1}".format(self.id, self.descripcion)

    class Meta:
        verbose_name_plural = "Ordenes de Trabajo"


class Actividad(models.Model):
    orden = models.ForeignKey(OrdenTrabajo)
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=144, null=True)
    horas_estimadas = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.0
    )
    horas_reales = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.0
    )
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
        return "{0} : {1}".format(self.orden, self.numero)

    class Meta:
        verbose_name_plural = "Actividades"
        unique_together = (('orden', 'numero'),)

    def _get_detalle_comentarios(self):

        detalles_fotos = ActividadDetalle.objects.filter(actividad=self).exclude(comentarios="")
        return detalles_fotos
    detalle_comentarios = property(_get_detalle_comentarios)

    def _get_detalle_fotos(self):
        detalles_fotos = ActividadDetalle.objects.filter(actividad=self).exclude(imagen="")
        return detalles_fotos
    detalle_fotos = property(_get_detalle_fotos)


class ActividadDetalle(models.Model):

    actividad = models.ForeignKey(Actividad)
    comentarios = models.TextField(null=True, blank=True)
    imagen = models.ImageField(
        upload_to='ordenes/actividades/imgs',
        blank=True,
        validators=[
            valid_extension,
            validate_image
        ]
    )
    # archivo = models.FileField(
    #     upload_to='ordenes/actividades/files',
    #     blank=True
    # )
    created_by = models.ForeignKey(User, null=True, blank=True)
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


class ManoObra(models.Model):
    orden = models.ForeignKey(OrdenTrabajo)
    empleado = models.ForeignKey(User, null=True)
    descripcion = models.CharField(max_length=144, null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    horas_estimadas = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.0,
        blank=True
    )
    horas_reales = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.0,
        blank=True
    )
    costo = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0, blank=True
    )

    # Auditoria Fields
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
        return "{0} : {1}".format(self.orden, self.empleado)

    class Meta:
        verbose_name_plural = "Mano de Obra"
        unique_together = (('orden', 'empleado'),)


class Material(models.Model):
    orden = models.ForeignKey(OrdenTrabajo)
    articulo = models.ForeignKey(Articulo)
    almacen = models.ForeignKey(Almacen, null=True)
    cantidad_estimada = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )
    cantidad_real = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )
    costo = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0, blank=True
    )
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
        return "{0} : {1}".format(self.orden, self.articulo)

    def _get_necesidad(self):
        return self.cantidad_estimada - self.cantidad_real
    necesidad = property(_get_necesidad)

    class Meta:
        verbose_name_plural = "Materiales"
        unique_together = (('orden', 'articulo'),)

    @receiver(post_save, sender=MovimientoDetalle)
    def crear_material(sender, instance, **kwards):

        if instance.cabecera.clasificacion == "OT":

            # Se buscar el articulo en materiales:
            material = Material.objects.filter(
                orden=instance.cabecera.orden_trabajo,
                articulo=instance.articulo,
            )

            # Si no se encentra:
            if len(material) == 0:

                # se genera en la orden:
                linea = Material()
                linea.orden = instance.cabecera.orden_trabajo
                linea.articulo = instance.articulo
                linea.cantidad_estimada = 0.0
                linea.save()


class ServicioExterno(models.Model):
    orden = models.ForeignKey(OrdenTrabajo)
    descripcion = models.CharField(max_length=144, null=True)
    clave_jde = models.CharField(max_length=144, null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    costo = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0, blank=True
    )
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
        clave = self.clave_jde
        return "{0} : {1}".format(self.orden, clave)

    class Meta:
        verbose_name_plural = "Servicios Externos"


class SolicitudCompraEncabezado(models.Model):

    descripcion = models.CharField(max_length=144)
    comentarios = models.TextField(null=True, blank=True)
    estado = models.CharField(
        max_length=4,
        choices=SOLICITUD_COMPRA_ESTADO,
        default="CAP",
        blank=True
    )
    solicitante = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="encabezado_created_by"
    )
    updated_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="encabezado_updated_by"
    )
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
        return self.descripcion


class SolicitudCompraDetalle(models.Model):
    cantidad = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0)
    articulo = models.ForeignKey(Articulo)
    comentarios = models.TextField(null=True, blank=True)
    encabezado = models.ForeignKey(SolicitudCompraEncabezado)
    created_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="sol_detalle_created_by"
    )
    updated_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="sol_detalle_updated_by"
    )
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

    class Meta:
        unique_together = (('articulo', 'encabezado'),)
