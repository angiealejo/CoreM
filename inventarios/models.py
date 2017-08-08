# -*- coding: utf-8 -*-

# Librerias Django:
from __future__ import unicode_literals
from django.db import models

# Otros modelos
from seguridad.models import Profile

# Validadores:
from home.validators import valid_extension
from home.validators import validate_image

# Historia
from simple_history.models import HistoricalRecords

# Signals
from django.db.models.signals import post_save
from django.dispatch import receiver


MOVIMIENTO_ESTADO = (
    ('CAP', 'CAPTURA'),
    ('CER', 'CERRADO'),
    ('TRAN', 'EN TRANSITO'),
)

MOVIMIENTO_TIPO = (
    ('ENT', 'ENTRADA'),
    ('SAL', 'SALIDA'),
)

MOVIMIENTO_CLASIFICACION = (
    ('SAL', 'SALDO INICIAL'),
    ('COM', 'COMPRA'),
    ('TRA', 'TRASPASO'),
    ('AJU', 'AJUSTE'),
    ('OT', 'ORDEN'),
    ('DES', 'DESPACHO A PERSONAL'),
)


class UdmArticulo(models.Model):
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

    def __unicode__(self):
        clave = self.clave
        desc = self.descripcion

        return "({}) {}".format(
            clave,
            desc
        )


class Articulo(models.Model):

    ARTICULO_TIPO = (
        ('CON', 'CONSUMIBLE'),
        ('REF', 'REFACCION'),
        ('HER', 'HERRAMIENTA'),
        ('EPP', 'EQUIPO DE PROTECCCION'),
    )

    ARTICULO_ESTADO = (
        ('ACT', 'ACTIVO'),
        ('DES', 'DESHABILITADO'),
    )

    clave = models.CharField(max_length=144, null=True, blank=True)
    descripcion = models.CharField(max_length=144, null=True, unique=True)
    estado = models.CharField(
        max_length=4,
        choices=ARTICULO_ESTADO,
        default="ACT",
    )
    tipo = models.CharField(
        max_length=6,
        choices=ARTICULO_TIPO,
        default="CORRE",
        blank=True
    )
    imagen = models.ImageField(
        upload_to='articulos/img',
        blank=True,
        null=True,
        validators=[
            valid_extension,
            validate_image
        ]
    )
    udm = models.ForeignKey(
        UdmArticulo,
        on_delete=models.PROTECT
    )
    url = models.URLField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    stock_seguridad = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0, blank=True)
    stock_minimo = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0, blank=True)
    stock_maximo = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0, blank=True)
    clave_jde = models.CharField(max_length=144, blank=True, null=True)
    marca = models.CharField(max_length=144, blank=True, null=True)
    modelo = models.CharField(max_length=144, blank=True, null=True)
    numero_parte = models.CharField(max_length=144, blank=True, null=True)
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

    def _get_cantidad_stock(self):
        try:
            stock = self.stock_set.get(
                almacen__descripcion__icontains="AGOSTO"
            )

            return stock.cantidad
        except Exception:
            return 0.0
    cantidad_stock = property(_get_cantidad_stock)

    def _get_faltantes_stock_seguridad(self):

        if self.stock_seguridad != 0.0:
            try:
                stock = self.stock_set.get(
                    almacen__descripcion__icontains="AGOSTO"
                )

                if self.stock_seguridad > stock.cantidad:
                    value = self.stock_seguridad - stock.cantidad
                    return value
                else:
                    return 0.0

            except Exception:
                return self.stock_seguridad
        else:
            return 0.0
    faltantes_stock_seguridad = property(_get_faltantes_stock_seguridad)

    def __unicode__(self):
        desc = self.descripcion
        return desc

    class Meta:
        verbose_name_plural = "Articulo"


class SeccionAlmacen(models.Model):

    clave = models.CharField(max_length=20, null=True)
    descripcion = models.CharField(max_length=144, null=True)
    asignado = models.BooleanField(default=False)

    def __unicode__(self):
        clave = self.clave
        desc = self.descripcion

        return "({0}) {1}".format(
            clave,
            desc
        )

    class Meta:
        verbose_name_plural = "Secciones Almacenes"


class Almacen(models.Model):

    ALMACEN_ESTADO = (
        ('ACT', 'ACTIVO'),
        ('DES', 'DESHABILITADO'),
    )
    clave = models.CharField(max_length=144, null=True)
    descripcion = models.CharField(max_length=144, null=True)
    # seccion = models.ManyToManyField(SeccionAlmacen, blank=True)
    estado = models.CharField(
        max_length=4,
        choices=ALMACEN_ESTADO,
        default="ACT",
        blank=True
    )
    articulos = models.ManyToManyField(
        Articulo,
        through="Stock",
        blank=True
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
        desc = self.descripcion
        estado = self.get_estado_display()
        if estado == "DESHABILITADO":
            return "%s (%s)" % (desc, estado)
        else:

            return "%s" % (desc)

    class Meta:
        verbose_name_plural = "Almacenes"


class Stock(models.Model):
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT)
    costo = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0, blank=True
    )
    cantidad = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0
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
        return "{0}) {1}".format(self.almacen, self.articulo)

    class Meta:
        unique_together = (('almacen', 'articulo'),)


@receiver(post_save, sender=Articulo)
def create_stock_articulo(sender, instance, **kwargs):

    # Se consultan los almacenes:
    almacenes = Almacen.objects.all()

    # Se crea stock con cantidad en 0:
    for r in almacenes:

        # consulta si existe stock por almacen:
        stock = Stock.objects.filter(
            articulo=instance,
            almacen=r
        )

        # Si no existe se crea
        if len(stock) == 0:

            s = Stock()
            s.articulo = instance
            s.almacen = r
            s.cantidad = 0.0
            s.save()


@receiver(post_save, sender=Almacen)
def create_stock_almacen(sender, instance, **kwargs):

    # Se consultan los articulo:
    articulos = Articulo.objects.all()

    # Se crea stock con cantidad en 0:
    for articulo in articulos:

        # consulta si existe stock por articulo:
        stock = Stock.objects.filter(
            almacen=instance,
            articulo=articulo
        )

        # Si no existe se crea
        if len(stock) == 0:

            stock = Stock()

            stock.almacen = instance
            stock.articulo = articulo
            stock.cantidad = 0.0
            stock.save()


class MovimientoCabecera(models.Model):
    fecha = models.DateTimeField()
    descripcion = models.CharField(max_length=144)
    almacen_origen = models.ForeignKey(
        Almacen, related_name="origen", null=True, blank=True)
    almacen_destino = models.ForeignKey(
        Almacen,
        related_name="destino",
        null=True,
        blank=True)
    persona_recibe = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="persona_entrega"
    )
    persona_entrega = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="persona_recibe"
    )
    proveedor = models.CharField(max_length=144, null=True, blank=True)
    estado = models.CharField(
        max_length=4,
        choices=MOVIMIENTO_ESTADO,
        default="CAP",
        blank=True
    )
    tipo = models.CharField(
        max_length=4,
        choices=MOVIMIENTO_TIPO,
    )
    clasificacion = models.CharField(
        max_length=4,
        choices=MOVIMIENTO_CLASIFICACION,
        default='AJU'
    )
    orden_trabajo = models.ForeignKey(
        'trabajos.OrdenTrabajo',
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="cabecera_created_by"
    )
    updated_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="cabecera_updated_by"
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
        desc = self.descripcion
        return desc


class MovimientoDetalle(models.Model):
    cantidad = models.DecimalField(
        max_digits=20, decimal_places=4, default=0.0)
    articulo = models.ForeignKey(Articulo)
    cabecera = models.ForeignKey(MovimientoCabecera)
    created_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="detalle_created_by"
    )
    updated_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        related_name="detalle_updated_by"
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
        unique_together = (('articulo', 'cabecera'),)
