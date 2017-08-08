# -*- coding: utf-8 -*-

# Django:
from django.forms import ModelForm
from django.forms import Form
from django.forms import TextInput
from django.forms import Select
from django.forms import CheckboxInput
from django.forms import Textarea
from django.forms import ChoiceField
from django.forms import CharField

from django import forms

# Modelos:
from .models import OrdenTrabajo
from .models import ActividadDetalle
from .models import SolicitudCompraEncabezado
from .models import SOLICITUD_COMPRA_ESTADO

# Otros Modelos:
from activos.models import Equipo
from seguridad.models import Profile
# from inventarios.models import Almacen

# ----------------- ORDEN DE TRABAJO ----------------- #


class OrdenTrabajoForm(ModelForm):

    class Meta:
        model = OrdenTrabajo
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'especialidad': Select(
                attrs={'class': 'form-control input-sm'}),
            'codigo_reporte': TextInput(
                attrs={'class': 'form-control input-sm'}),
            'equipo': Select(attrs={'class': 'form-control input-sm'}),
            'tipo': Select(attrs={'class': 'form-control input-sm select2'}),
            'estado': Select(attrs={'class': 'form-control input-sm select2'}),
            'permiso': TextInput(attrs={'class': 'form-control input-sm'}),
            'fecha_estimada_inicio': TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'data-date-format': 'yyyy-mm-dd'
                }
            ),
            'fecha_estimada_fin': TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'data-date-format': 'yyyy-mm-dd'
                }
            ),
            'fecha_real_inicio': TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'data-date-format': 'yyyy-mm-dd'
                }
            ),
            'fecha_real_fin': TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'data-date-format': 'yyyy-mm-dd'
                }
            ),
            'es_template': CheckboxInput(),
            'responsable': Select(
                attrs={'class': 'form-control input-sm select2'}),
            'solicitante': Select(
                attrs={'class': 'form-control input-sm select2'}),
            'observaciones': Textarea(
                attrs={'class': 'form-control input-sm'}
            ),
            'motivo_cancelacion': Textarea(
                attrs={'class': 'form-control input-sm'}
            ),
        }
        labels = {
            'es_template': "Template",
            'permiso': 'Permiso HSE',
            'codigo_reporte': 'Código Reporte',
        }

    def clean_motivo_cancelacion(self):
        cleaned_data = super(OrdenTrabajoForm, self).clean()
        motivo_cancelacion = cleaned_data.get('motivo_cancelacion')
        estado = cleaned_data.get('estado')

        if estado == "CAN" and motivo_cancelacion is None:
            raise forms.ValidationError(
                "Favor de mencionar el motivo por el cual se esta cancelando la Orden"
            )

        if estado == "CAN" and motivo_cancelacion == "":
            raise forms.ValidationError(
                "Favor de mencionar el motivo por el cual se esta cancelando la Orden"
            )

        return motivo_cancelacion


class OrdenTrabajoFiltersForm(Form):
    numero_orden = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    tipo = ChoiceField(
        widget=Select(attrs={'class': 'form-control input-sm  select2'})
    )
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    especialidad = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    equipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    responsable = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    solicitante = ChoiceField(
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

    def __init__(self, *args, **kwargs):

        super(OrdenTrabajoFiltersForm, self).__init__(*args, **kwargs)
        self.fields['equipo'].choices = self.get_Equipos()
        self.fields['responsable'].choices = self.get_Users()
        self.fields['solicitante'].choices = self.get_Users()
        self.fields['tipo'].choices = self.get_Tipos(OrdenTrabajo.ORDEN_TIPO)
        self.fields['estado'].choices = self.get_Estados(
            OrdenTrabajo.ORDEN_ESTADO
        )
        self.fields['especialidad'].choices = self.get_Estados(
            OrdenTrabajo.ORDEN_ESPECIALIDAD
        )

    def get_Tipos(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones

    def get_Equipos(self):

        equipo = [('', '-------')]

        registros = Equipo.objects.all()

        for registro in registros:
            equipo.append(
                (
                    registro.pk,
                    "(%s) {%s} " % (registro.tag, registro.descripcion)
                )
            )

        return equipo

    def get_Users(self):

        usuarios = [('', '-------')]

        registros = Profile.objects.all()

        for registro in registros:
            usuarios.append(
                (
                    registro.user.id,
                    registro.user.get_full_name()
                )
            )

        return usuarios


class ActividadDetalleForm(ModelForm):

    class Meta:
        model = ActividadDetalle
        fields = [
            'comentarios',
            'imagen',
        ]
        exclude = [
            'actividad'
        ]
        widgets = {
            'comentarios': Textarea(
                attrs={'class': 'form-control input-sm'}
            )
        }


class SolicitudCompraEncabezadoFiltersForm(Form):

    fecha_inicio = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right input-sm',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    estado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    solicitante = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(SolicitudCompraEncabezadoFiltersForm, self).__init__(
            *args, **kwargs)
        self.fields['solicitante'].choices = self.get_Users()
        self.fields['estado'].choices = self.get_Estados(
            SOLICITUD_COMPRA_ESTADO)

    def get_Estados(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones

    def get_Users(self):

        usuarios = [('', '-------')]

        registros = Profile.objects.all()

        for registro in registros:
            usuarios.append(
                (

                    registro.user.id,
                    registro.user.get_full_name()
                )
            )

        return usuarios


class SolicitudCompraEncabezadoForm(ModelForm):

    class Meta:
        model = SolicitudCompraEncabezado
        fields = [
            'descripcion',
            'comentarios',
            'solicitante'
        ]
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'comentarios': Textarea(attrs={'class': 'form-control input-sm'}),
            'solicitante': Select(attrs={'class': 'form-control input-sm'}),
        }
        labels = {
            'descripcion': 'Descripción',
            'comentarios': 'Comentarios',
        }
