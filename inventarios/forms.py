# -*- coding: utf-8 -*-

# Django:
from django.forms import ModelForm
from django.forms import TextInput
from django.forms import Select
# from django.forms import SelectMultiple
from django.forms import ChoiceField
from django.forms import Textarea
from django.forms import CharField
from django.forms import Form
from django.forms import URLInput


# Modelos:
from .models import Almacen
from .models import Articulo
from .models import UdmArticulo
from .models import MovimientoCabecera
# from .models import MovimientoDetalle
from .models import MOVIMIENTO_ESTADO
from .models import MOVIMIENTO_CLASIFICACION
from .models import MOVIMIENTO_TIPO
# from .models import SeccionAlmacen
from trabajos.models import OrdenTrabajo
from seguridad.models import Profile

ALMACEN_ESTADO = (
    ('ACT', 'ACTIVO'),
    ('DES', 'DESHABILITADO'),
)
# ----------------- ALMACEN ----------------- #


class AlmacenForm(ModelForm):

    class Meta:
        model = Almacen
        fields = [
            'clave',
            'descripcion',
            'estado',
        ]
        widgets = {
            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'estado': Select(attrs={'class': 'form-control input-sm'}),
        }


# ----------------- UDM ODOMETRO ----------------- #

class UdmArticuloForm(ModelForm):

    class Meta:
        model = UdmArticulo
        fields = '__all__'
        widgets = {
            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
        }


# ----------------- ARTICULO ----------------- #

class ArticuloFilterForm(ModelForm):

    class Meta:
        model = Articulo
        fields = [
            'clave',
            'descripcion',
            'tipo',
            'clave_jde',
            'estado',
            'imagen',
            'marca',
            'modelo',
            'numero_parte',
        ]
        widgets = {
            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'tipo': Select(attrs={'class': 'form-control input-sm'}),
            'clave_jde': TextInput(attrs={'class': 'form-control input-sm'}),
        }


class ArticuloForm(ModelForm):

    class Meta:
        model = Articulo
        fields = [
            'clave',
            'descripcion',
            'tipo',
            'udm',
            'observaciones',
            'url',
            'marca',
            'modelo',
            'numero_parte',
            'stock_seguridad',
            'stock_minimo',
            'stock_maximo',
            'clave_jde',
            'estado',
            'imagen',
        ]
        widgets = {
            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'tipo': Select(attrs={'class': 'form-control input-sm'}),
            'udm': Select(attrs={'class': 'form-control input-sm'}),
            'observaciones': Textarea(
                attrs={'class': 'form-control input-sm'}),
            'url': URLInput(attrs={'class': 'form-control input-sm', 'placeholder':'http://www.website.com'}),
            'stock_seguridad': TextInput(
                attrs={'class': 'form-control input-sm', 'type': 'number'}),
            'stock_minimo': TextInput(
                attrs={'class': 'form-control input-sm', 'type': 'number'}),
            'stock_maximo': TextInput(
                attrs={'class': 'form-control input-sm', 'type': 'number'}),
            'clave_jde': TextInput(attrs={'class': 'form-control input-sm'}),
            'estado': Select(attrs={'class': 'form-control input-sm'}),
            'marca': TextInput(attrs={'class': 'form-control input-sm'}),
            'modelo': TextInput(attrs={'class': 'form-control input-sm'}),
            'numero_parte': TextInput(attrs={'class': 'form-control input-sm'}),
        }
        labels = {
            'clave_jde': 'Clave JDE',
            'stock_seguridad': 'Stock de Seguridad',
            'numero_parte': 'No. Parte',
            'stock_minimo': 'Stock Mínimo',
            'stock_maximo': 'Stock Máximo',
            'url': 'URL'
        }


# ----------------- STOCK ----------------- #

class StockFilterForm(Form):

    almacen = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    articulo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    cantidad_menorque = CharField(
        widget=TextInput(
            attrs={'class': 'form-control input-sm'})
    )

    cantidad_mayorque = CharField(
        widget=TextInput(
            attrs={'class': 'form-control input-sm'})
    )

    def __init__(self, *args, **kwargs):
        super(StockFilterForm, self).__init__(*args, **kwargs)
        self.fields['articulo'].choices = self.obtener_Articulos()
        self.fields['almacen'].choices = self.obtener_Almacenes()

    def obtener_Articulos(self):

        articulo = [('', 'Todos'), ]

        registros = Articulo.objects.all()

        for registro in registros:
            if registro.clave is None:
                clave = "-"
            else:
                clave = registro.clave
            articulo.append(
                (
                    registro.id,
                    "(%s) %s" % (clave, registro.descripcion)
                )
            )

        return articulo

    def obtener_Almacenes(self):

        articulo = [('', 'Todos'), ]

        registros = Almacen.objects.all()

        for registro in registros:
            articulo.append(
                (
                    registro.id,
                    "(%s) %s" % (registro.clave, registro.descripcion)
                )
            )

        return articulo


# ----------------- ENTRADAS ----------------- #

class EntradaSaldoFiltersForm(Form):

    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    almacen_destino = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(EntradaSaldoFiltersForm, self).__init__(*args, **kwargs)
        self.fields['almacen_destino'].choices = self.get_Almacenes()
        self.fields['estado'].choices = self.get_Estados(MOVIMIENTO_ESTADO)

    def get_Almacenes(self):
        almacen_destino = [('', '-------')]

        registros = Almacen.objects.all()

        for registro in registros:
            almacen_destino.append(
                (
                    registro.id,
                    "%s" % (registro.descripcion)
                )
            )

        return almacen_destino

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones


class EntradaSaldoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EntradaSaldoForm, self).__init__(*args, **kwargs)
        self.fields['almacen_destino'].required = True

    class Meta:
        model = MovimientoCabecera
        fields = [
            'descripcion',
            'almacen_destino',
            'fecha',
        ]
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'almacen_destino': Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'fecha': TextInput(attrs={'class': 'form-control input-sm',
                                      'data-date-format': 'yyyy-mm-dd'}),
        }


class EntradaCompraFiltersForm(Form):

    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    almacen_destino = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    proveedor = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    persona_recibe = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(EntradaCompraFiltersForm, self).__init__(*args, **kwargs)
        self.fields['almacen_destino'].choices = self.get_Almacenes()
        self.fields['persona_recibe'].choices = self.get_Profiles()
        self.fields['estado'].choices = self.get_Estados(MOVIMIENTO_ESTADO)

    def get_Almacenes(self):
        almacen_destino = [('', '-------')]

        registros = Almacen.objects.all()

        for registro in registros:
            almacen_destino.append(
                (
                    registro.id,
                    "%s" % (registro.descripcion)
                )
            )

        return almacen_destino

    def get_Profiles(self):
        persona_recibe = [('', '-------')]

        registros = Profile.objects.all()

        for registro in registros:
            persona_recibe.append(
                (
                    registro.id,
                    registro.user.get_full_name()
                )
            )

        return persona_recibe

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones


class EntradaCompraForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EntradaCompraForm, self).__init__(*args, **kwargs)
        self.fields['almacen_destino'].required = True

    class Meta:
        model = MovimientoCabecera
        fields = [
            'descripcion',
            'fecha',
            'almacen_destino',
            'proveedor',
            'persona_recibe',
        ]
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'almacen_destino': Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'fecha': TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'data-date-format': 'yyyy-mm-dd'
                }
            ),
            'proveedor': TextInput(attrs={'class': 'form-control input-sm'}),
            'persona_recibe': Select(
                attrs={'class': 'form-control input-sm'}
            ),
        }


class EntradaAjusteFiltersForm(Form):

    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    almacen_destino = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(EntradaAjusteFiltersForm, self).__init__(*args, **kwargs)
        self.fields['almacen_destino'].choices = self.get_Almacenes()
        self.fields['estado'].choices = self.get_Estados(MOVIMIENTO_ESTADO)

    def get_Almacenes(self):
        almacen_destino = [('', '-------')]

        registros = Almacen.objects.all()

        for registro in registros:
            almacen_destino.append(
                (
                    registro.id,
                    "%s" % (registro.descripcion)
                )
            )

        return almacen_destino

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones


class EntradaAjusteForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EntradaAjusteForm, self).__init__(*args, **kwargs)
        self.fields['almacen_destino'].required = True

    class Meta:
        model = MovimientoCabecera
        fields = [
            'descripcion',
            'almacen_destino',
            'fecha',
        ]
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'almacen_destino': Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'fecha': TextInput(attrs={'class': 'form-control input-sm',
                                      'data-date-format': 'yyyy-mm-dd'}),
        }


class EntradaTraspasoFiltersForm(Form):
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    almacen_origen = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    almacen_destino = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    persona_entrega = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    persona_recibe = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(EntradaTraspasoFiltersForm, self).__init__(*args, **kwargs)
        self.fields['estado'].choices = self.get_Estados(MOVIMIENTO_ESTADO)
        self.fields['almacen_origen'].choices = self.get_Almacenes()
        self.fields['almacen_destino'].choices = self.get_Almacenes()
        self.fields['persona_entrega'].choices = self.get_Profiles()
        self.fields['persona_recibe'].choices = self.get_Profiles()

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones

    def get_Almacenes(self):
        almacen = [('', '-------')]

        registros = Almacen.objects.all()

        for registro in registros:
            almacen.append(
                (
                    registro.id,
                    "%s" % (registro.descripcion)
                )
            )

        return almacen

    def get_Profiles(self):
        persona = [('', '-------')]

        registros = Profile.objects.all()

        for registro in registros:
            persona.append(
                (
                    registro.id,
                    registro.user.get_full_name()
                )
            )

        return persona


# ----------------- MOVIMIENTOS ----------------- #

class InventarioFiltersForm(Form):
    tipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    descripcion_encabezado = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    almacen_destino = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    almacen_origen = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    proveedor = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    persona_recibe = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    persona_entrega = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    articulo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    orden_trabajo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    clasificacion = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(InventarioFiltersForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].choices = self.get_Tipo(MOVIMIENTO_TIPO)
        self.fields['almacen_destino'].choices = self.get_Almacenes()
        self.fields['almacen_origen'].choices = self.get_Almacenes()
        self.fields['persona_entrega'].choices = self.get_Profiles()
        self.fields['persona_recibe'].choices = self.get_Profiles()
        self.fields['orden_trabajo'].choices = self.get_Ordenes()
        self.fields['estado'].choices = self.get_Estados(MOVIMIENTO_ESTADO)
        self.fields['clasificacion'].choices = self.get_Clasificacion(
            MOVIMIENTO_CLASIFICACION)
        self.fields['articulo'].choices = self.get_Articulos()

    def get_Tipo(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones

    def get_Almacenes(self):
        almacen_destino = [('', '-------')]

        registros = Almacen.objects.all()

        for registro in registros:
            almacen_destino.append(
                (
                    registro.id,
                    "%s" % (registro.descripcion)
                )
            )

        return almacen_destino

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones

    def get_Profiles(self):
        persona = [('', '-------')]

        registros = Profile.objects.all()

        for registro in registros:

            persona.append(
                (
                    registro.id,
                    registro.user.get_full_name()
                )
            )

        return persona

    def get_Ordenes(self):
        orden_trabajo = [('', '-------')]

        registros = OrdenTrabajo.objects.all()

        for registro in registros:
            value = "(%s) %s" % (registro.equipo, registro.descripcion)
            orden_trabajo.append(
                (
                    registro.id,
                    value
                )
            )

        return orden_trabajo

    def get_Clasificacion(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones

    def get_Articulos(self):
        articulo = [('', '-------')]

        registros = Articulo.objects.all()

        for registro in registros:

            if registro.clave is None:
                clave = "-"
            else:
                clave = registro.clave

            articulo.append(
                (
                    registro.id,
                    "(%s) %s" % (clave, registro.descripcion)
                )
            )

        return articulo


class InventarioForm(ModelForm):

    class Meta:
        model = MovimientoCabecera
        fields = [
            'tipo',
            'clasificacion',
            'descripcion',
            'almacen_origen',
            'almacen_destino',
            'fecha',
            'persona_recibe',
            'persona_entrega',
            'proveedor'
        ]
        widgets = {
            'tipo': Select(attrs={'class': 'form-control input-sm'}),
            'clasificacion': Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'almacen_origen': Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'almacen_destino': Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'fecha': TextInput(attrs={'class': 'form-control input-sm',
                                      'data-date-format': 'yyyy-mm-dd'}),
            'persona_recibe': Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'persona_entrega': Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'proveedor': TextInput(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
        }
        labels = {
            'clasificacion': 'Clasificación',
            'descripcion': 'Descripción',
        }


# ------------------------ SALIDAS -------------------------- #


class SalidaPersonalFiltersForm(Form):
    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    almacen_origen = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    persona_entrega = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    persona_recibe = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(SalidaPersonalFiltersForm, self).__init__(*args, **kwargs)
        self.fields['almacen_origen'].choices = self.get_Almacenes()
        self.fields['persona_recibe'].choices = self.get_Profiles()
        self.fields['persona_entrega'].choices = self.get_Profiles()
        self.fields['estado'].choices = self.get_Estados(MOVIMIENTO_ESTADO)

    def get_Almacenes(self):
        almacen_destino = [('', '-------')]

        registros = Almacen.objects.all()

        for registro in registros:
            almacen_destino.append(
                (
                    registro.id,
                    "%s" % (registro.descripcion)
                )
            )

        return almacen_destino

    def get_Profiles(self):
        persona_recibe = [('', '-------')]

        registros = Profile.objects.all()

        for registro in registros:
            persona_recibe.append(
                (
                    registro.id,
                    registro.user.get_full_name()
                )
            )

        return persona_recibe

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones


class SalidaPersonalForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SalidaPersonalForm, self).__init__(*args, **kwargs)
        self.fields['almacen_origen'].required = True
        self.fields['persona_entrega'].required = True
        self.fields['persona_recibe'].required = True

    class Meta:
        model = MovimientoCabecera
        fields = [
            'descripcion',
            'fecha',
            'almacen_origen',
            'persona_entrega',
            'persona_recibe',
        ]
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'almacen_origen': Select(attrs={'class': 'form-control input-sm'}),
            'fecha': TextInput(attrs={'class': 'form-control input-sm',
                                      'data-date-format': 'yyyy-mm-dd'}),
            'persona_entrega': Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'persona_recibe': Select(attrs={'class': 'form-control input-sm'}),
        }


class SalidaOrdenTrabajoFiltersForm(Form):
    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    almacen_origen = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    persona_entrega = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    persona_recibe = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    orden_trabajo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(SalidaOrdenTrabajoFiltersForm, self).__init__(*args, **kwargs)
        self.fields['almacen_origen'].choices = self.get_Almacenes()
        self.fields['persona_recibe'].choices = self.get_Profiles()
        self.fields['estado'].choices = self.get_Estados(MOVIMIENTO_ESTADO)
        self.fields['orden_trabajo'].choices = self.get_Ordenes()

    def get_Almacenes(self):
        almacen_destino = [('', '-------')]

        registros = Almacen.objects.all()

        for registro in registros:
            almacen_destino.append(
                (
                    registro.id,
                    "%s" % (registro.descripcion)
                )
            )

        return almacen_destino

    def get_Profiles(self):
        persona_recibe = [('', '-------')]

        registros = Profile.objects.all()

        for registro in registros:
            persona_recibe.append(
                (
                    registro.id,
                    registro.user.get_full_name()
                )
            )

        return persona_recibe

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones

    def get_Ordenes(self):
        orden_trabajo = [('', '-------')]

        registros = OrdenTrabajo.objects.all()

        for registro in registros:
            orden_trabajo.append(
                (
                    registro.id,
                    "(%s) %s" % (registro.id, registro.descripcion)
                )
            )

        return orden_trabajo


class SalidaOrdenTrabajoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SalidaOrdenTrabajoForm, self).__init__(*args, **kwargs)
        self.fields['orden_trabajo'].required = True
        self.fields['almacen_origen'].required = True
        self.fields['persona_entrega'].required = True
        self.fields['persona_recibe'].required = True

    class Meta:
        model = MovimientoCabecera
        fields = [
            'descripcion',
            'fecha',
            'almacen_origen',
            'persona_entrega',
            'persona_recibe',
            'orden_trabajo',
        ]
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'almacen_origen': Select(attrs={'class': 'form-control input-sm'}),
            'fecha': TextInput(attrs={'class': 'form-control input-sm',
                                      'data-date-format': 'yyyy-mm-dd'}),
            'persona_entrega': Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'persona_recibe': Select(attrs={'class': 'form-control input-sm'}),
            'orden_trabajo': Select(attrs={'class': 'form-control input-sm'}),
        }


class SalidaAjusteFiltersForm(Form):

    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    almacen_origen = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(SalidaAjusteFiltersForm, self).__init__(*args, **kwargs)
        self.fields['almacen_origen'].choices = self.get_Almacenes()
        self.fields['estado'].choices = self.get_Estados(MOVIMIENTO_ESTADO)

    def get_Almacenes(self):
        almacen_destino = [('', '-------')]

        registros = Almacen.objects.all()

        for registro in registros:
            almacen_destino.append(
                (
                    registro.id,
                    "%s" % (registro.descripcion)
                )
            )

        return almacen_destino

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones


class SalidaAjusteForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SalidaAjusteForm, self).__init__(*args, **kwargs)
        self.fields['almacen_origen'].required = True

    class Meta:
        model = MovimientoCabecera
        fields = [
            'descripcion',
            'almacen_origen',
            'fecha',
        ]
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'almacen_origen': Select(attrs={'class': 'form-control input-sm'}),
            'fecha': TextInput(attrs={'class': 'form-control input-sm',
                                      'data-date-format': 'yyyy-mm-dd'}),
        }


class SalidaTraspasoFiltersForm(Form):

    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    almacen_origen = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    almacen_destino = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    persona_entrega = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    persona_recibe = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(SalidaTraspasoFiltersForm, self).__init__(*args, **kwargs)
        self.fields['almacen_origen'].choices = self.get_Almacenes()
        self.fields['almacen_destino'].choices = self.get_Almacenes()
        self.fields['persona_entrega'].choices = self.get_Profiles()
        self.fields['persona_recibe'].choices = self.get_Profiles()
        self.fields['estado'].choices = self.get_Estados(MOVIMIENTO_ESTADO)

    def get_Almacenes(self):
        almacen = [('', '-------')]

        registros = Almacen.objects.all()

        for registro in registros:
            almacen.append(
                (
                    registro.id,
                    "%s" % (registro.descripcion)
                )
            )

        return almacen

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones

    def get_Profiles(self):
        persona = [('', '-------')]

        registros = Profile.objects.all()

        for registro in registros:
            persona.append(
                (
                    registro.id,
                    registro.user.get_full_name()
                )
            )

        return persona


class SalidaTraspasoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SalidaTraspasoForm, self).__init__(*args, **kwargs)
        self.fields['almacen_origen'].required = True
        self.fields['almacen_destino'].required = True

    class Meta:
        model = MovimientoCabecera
        fields = [
            'descripcion',
            'almacen_origen',
            'almacen_destino',
            'persona_entrega',
            'persona_recibe',
            'fecha',
        ]
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'almacen_origen': Select(attrs={'class': 'form-control input-sm'}),
            'almacen_destino': Select(
                attrs={
                    'class': 'form-control input-sm'
                }),
            'persona_entrega': Select(
                attrs={
                    'class': 'form-control input-sm'
                }),
            'persona_recibe': Select(attrs={'class': 'form-control input-sm'}),
            'fecha': TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'data-date-format': 'yyyy-mm-dd'
                })
        }
