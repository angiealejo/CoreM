# -*- coding: utf-8 -*-

# Django:
from django.forms import ModelForm
from django.forms import Form
from django.forms import TextInput
from django.forms import Select
from django.forms import CheckboxInput
from django.forms import CharField
from django.forms import ChoiceField
from django.forms import ValidationError

# Modelos:
from .models import Equipo
from .models import Odometro
from .models import Medicion
from .models import Ubicacion
from .models import UdmOdometro
from .models import TipoOdometro
from .models import TipoEquipo
# from .models import OdometroAsignacion


# ----------------- EQUIPO ----------------- #

class EquipoFiltersForm(ModelForm):

    class Meta:
        model = Equipo
        fields = [
            'tag',
            'descripcion',
            'serie',
            'estado',
            'tipo',
            'padre',
            'sistema',
            'ubicacion',
        ]
        widgets = {
            'tag': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'serie': TextInput(attrs={'class': 'form-control input-sm'}),
            'estado': Select(attrs={'class': 'form-control input-sm select2'}),
            'tipo': Select(attrs={'class': 'form-control input-sm select2'}),
            'padre': Select(attrs={'class': 'form-control input-sm select2'}),
            'sistema': TextInput(attrs={'class': 'form-control input-sm'}),
            'ubicacion': Select(
                attrs={'class': 'form-control input-sm select2'}
            ),
        }
        labels = {
            'tag': 'Tag',
            'descripcion': 'Descripción',
            'serie': 'Serie',
            'estado': 'Estado',
            'tipo': 'Tipo',
            'padre': 'Padre',
            'sistema': 'Sistema',
            'ubicacion': 'Ubicación',
        }


class EquipoForm(ModelForm):

    class Meta:
        model = Equipo
        fields = '__all__'
        widgets = {
            'tag': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'serie': TextInput(attrs={'class': 'form-control input-sm'}),
            'especialidad': TextInput(attrs={'class': 'form-control input-sm'}),
            'estado': Select(attrs={'class': 'form-control input-sm select2'}),
            'tipo': Select(attrs={'class': 'form-control input-sm select2'}),
            'padre': Select(attrs={'class': 'form-control input-sm select2'}),
            'contrato': Select(attrs={'class': 'form-control input-sm select2'}),
            'sistema': TextInput(attrs={'class': 'form-control input-sm'}),
            'ubicacion': Select(
                attrs={'class': 'form-control input-sm select2'}
            ),
            'cliente': TextInput(attrs={'class': 'form-control input-sm'}),
            'responsable': Select(attrs={'class': 'form-control input-sm select2'}),
        }
        labels = {
            'tag': 'Tag',
            'descripcion': 'Descripción',
            'serie': 'Serie',
            'especialidad': 'Especialidad',
            'estado': 'Estado',
            'tipo': 'Tipo',
            'padre': 'Padre',
            'sistema': 'Sistema',
            'ubicacion': 'Ubicación',
            'imagen': 'Imagen',
            'cliente': 'Cliente',
            'responsable': 'Responsable',
        }


# ----------------- ODÓMETRO ----------------- #

class OdometroForm(ModelForm):

    class Meta:
        model = Odometro
        fields = [
            'clave',
            'descripcion',
            'udm',
            'esta_activo',
            'acumulado',
            'tipo',
            'clasificacion',
        ]
        widgets = {
            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
            'udm': Select(attrs={'class': 'form-control input-sm select2'}),
            'esta_activo': CheckboxInput(),
            'acumulado': Select(attrs={'class': 'form-control input-sm select2'}),
            'tipo': Select(attrs={'class': 'form-control input-sm select2'}),
            'clasificacion': Select(attrs={'class': 'form-control input-sm select2'}),

        }
        labels = {
            'clave': 'Clave',
            'descripcion': 'Descripción',
            'udm': 'UDM',
            'esta_activo': 'Activo',
            'clasificacion': 'Clasificación',
        }


class OdometroFiltersForm(Form):

    clave = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    descripcion = CharField(
        widget=TextInput(attrs={'class': 'form-control input-sm'})
    )
    udm = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    equipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    tipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )
    acumulado = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm  select2'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(OdometroFiltersForm, self).__init__(*args, **kwargs)
        self.fields['equipo'].choices = self.get_Equipos()
        self.fields['udm'].choices = self.get_Udm()
        self.fields['tipo'].choices = self.get_Tipos()
        self.fields['acumulado'].choices = self.get_Acumulado(Odometro.ACUMULADO)

    def get_Equipos(self):

        equipo = [('', '-------')]

        registros = Equipo.objects.all()

        for registro in registros:
            equipo.append(
                (
                    registro.pk,
                    "(%s) %s" % (registro.tag, registro.descripcion)
                )
            )

        return equipo

    def get_Udm(self):

        udm = [('', '-------')]

        registros = UdmOdometro.objects.all()

        for registro in registros:
            udm.append(
                (
                    registro.id,
                    "(%s) %s" % (registro.clave, registro.descripcion)
                )
            )

        return udm

    def get_Tipos(self):

        tipo = [('', '-------')]

        registros = TipoOdometro.objects.all()

        for registro in registros:
            tipo.append(
                (
                    registro.id,
                    "(%s) %s" % (registro.clave, registro.descripcion)
                )
            )

        return tipo

    def get_Acumulado(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones


# ----------------- UDM ODOMETRO ----------------- #

class UdmOdometroForm(ModelForm):

    class Meta:
        model = UdmOdometro
        fields = '__all__'
        widgets = {
            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
        }


# ----------------- MEDICION ----------------- #

class MedicionFiltersForm(Form):

    equipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm', 'multiple': 'multiple'}
        )
    )
    odometro = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm', 'multiple': 'multiple'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(
            attrs={'class': 'form-control input-sm', 'required': 'required', 'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(
            attrs={'class': 'form-control input-sm', 'required': 'required', 'data-date-format': 'yyyy-mm-dd'})
    )
    tipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'})
    )

    def __init__(self, *args, **kwargs):

        super(MedicionFiltersForm, self).__init__(*args, **kwargs)
        self.fields['equipo'].choices = self.get_Equipos()
        self.fields['odometro'].choices = self.get_Odometros()
        self.fields['tipo'].choices = self.get_Tipos()

    def get_Equipos(self):

        equipo = []

        registros = Equipo.objects.all()

        for registro in registros:
            equipo.append(
                (
                    registro.pk,
                    "(%s) %s " % (registro.tag, registro.descripcion)
                )
            )

        return equipo

    def get_Odometros(self):

        odometro = []

        registros = Odometro.objects.all()

        for registro in registros:
            odometro.append(
                (
                    registro.id,
                    "(%s) %s " % (registro.clave, registro.descripcion)
                )
            )

        return odometro

    def get_Tipos(self):

        tipo = [('0', '--------')]

        registros = TipoOdometro.objects.all()

        for registro in registros:
            tipo.append(
                (
                    registro.id,
                    "(%s) %s " % (registro.clave, registro.descripcion)
                )
            )

        return tipo


class MedicionForm(ModelForm):

    class Meta:
        model = Medicion
        fields = [
            'fecha',
            'lectura'
        ]
        widgets = {
            'fecha': TextInput(
                attrs={
                    'class': 'form-control input-sm pull-right',
                    'data-date-format': 'yyyy-mm-dd'
                }
            ),
            'lectura': TextInput(attrs={'class': 'form-control input-sm'}),
        }
        labels = {
            'fecha': 'Fecha',
            'lectura': 'Lectura',
        }


# ----------------- UBICACION ----------------- #

class UbicacionForm(ModelForm):

    class Meta:
        model = Ubicacion
        fields = '__all__'
        widgets = {
            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
        }


class TipoOdometroForm(ModelForm):

    class Meta:
        model = TipoOdometro
        fields = [
            'clave',
            'descripcion',
        ]
        widgets = {
            'clave': TextInput(attrs={'class': 'form-control input-sm'}),
            'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
        }


class CapturaFiltersForm(Form):

    equipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm', 'required': 'required'}
        )
    )
    tipo_equipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(
            attrs={'class': 'form-control input-sm', 'required': 'required', 'data-date-format': 'yyyy-mm-dd'})
    )
    fecha_fin = CharField(
        widget=TextInput(
            attrs={'class': 'form-control input-sm', 'required': 'required', 'data-date-format': 'yyyy-mm-dd'})
    )
    tipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'})
    )

    def __init__(self, *args, **kwargs):

        super(CapturaFiltersForm, self).__init__(*args, **kwargs)
        # self.fields['equipo'].choices = self.get_Equipos()
        self.fields['tipo_equipo'].choices = self.get_TiposEquipo()
        self.fields['tipo'].choices = self.get_Tipos()

    def clean_equipo(self):
        data = self.cleaned_data['equipo']
        if data == 0:
            raise ValidationError("Debe seleccionar un equipo")
        else:
            return data

    def get_TiposEquipo(self):

        tipo = []

        registros = TipoEquipo.objects.all()

        for registro in registros:
            tipo.append(
                (
                    registro.pk,
                    "(%s) %s " % (registro.clave, registro.descripcion)
                )
            )

        return tipo

    def get_Odometros(self):

        odometro = []

        registros = Odometro.objects.all()

        for registro in registros:
            odometro.append(
                (
                    registro.id,
                    "(%s) %s " % (registro.clave, registro.descripcion)
                )
            )

        return odometro

    def get_Tipos(self):

        tipo = [('0', '--------')]

        registros = TipoOdometro.objects.all()

        for registro in registros:
            tipo.append(
                (
                    registro.id,
                    "(%s) %s " % (registro.clave, registro.descripcion)
                )
            )

        return tipo


class VerificacionFiltersForm(Form):
    TYPES = (
        ('+', 'CREACIÓN'),
        ('~', 'EDICIÓN'),
        ('-', 'BORRADO'),

    )
    equipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm', 'required': 'required'}
        )
    )
    tipo_equipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )
    fecha_inicio = CharField(
        widget=TextInput(
            attrs={'class': 'form-control input-sm', 'required': 'required'})
    )
    fecha_fin = CharField(
        widget=TextInput(
            attrs={'class': 'form-control input-sm', 'required': 'required'})
    )
    tipo = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'})
    )
    history_type = ChoiceField(
        widget=Select(
            attrs={'class': 'form-control input-sm'}
        )
    )

    def __init__(self, *args, **kwargs):

        super(VerificacionFiltersForm, self).__init__(*args, **kwargs)
        self.fields['tipo_equipo'].choices = self.get_TiposEquipo()
        self.fields['tipo'].choices = self.get_Tipos()
        self.fields['history_type'].choices = self.get_HistoryType(self.TYPES)
        self.fields['history_type'].label = "Operación"

    def clean_equipo(self):
        data = self.cleaned_data['equipo']
        if data == 0:
            raise ValidationError("Debe seleccionar un equipo")
        else:
            return data

    def get_TiposEquipo(self):

        tipo = []

        registros = TipoEquipo.objects.all()

        for registro in registros:
            tipo.append(
                (
                    registro.pk,
                    "(%s) %s " % (registro.clave, registro.descripcion)
                )
            )

        return tipo

    def get_Odometros(self):

        odometro = []

        registros = Odometro.objects.all()

        for registro in registros:
            odometro.append(
                (
                    registro.id,
                    "(%s) %s " % (registro.clave, registro.descripcion)
                )
            )

        return odometro

    def get_Tipos(self):

        tipo = [('0', '--------')]

        registros = TipoOdometro.objects.all()

        for registro in registros:
            tipo.append(
                (
                    registro.id,
                    "(%s) %s " % (registro.clave, registro.descripcion)
                )
            )

        return tipo

    def get_HistoryType(self, _opciones):
        opciones = [('', '-------')]

        for registro in _opciones:
            opciones.append(registro)
        return opciones
# ----------------- SISTEMA ----------------- #

# class SistemaForm(ModelForm):

#     class Meta:
#         model = Sistema
#         fields = '__all__'
#         exclude = [
#             'created_date',
#             'created_by',
#             'updated_date',
#             'updated_by',
#         ]
#         widgets = {
#             'clave': TextInput(attrs={'class': 'form-control input-sm'}),
#             'descripcion': TextInput(attrs={'class': 'form-control input-sm'}),
#         }
