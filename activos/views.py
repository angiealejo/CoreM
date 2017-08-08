# -*- coding: utf-8 -*-
# _*_ coding: utf-8

from __future__ import unicode_literals

import xlwt
import xlsxwriter
import json
import datetime

# Django settings
from django.conf import settings

# Django Atajos:
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

# Django Urls:
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse


# Django Generic Views
from django.views.generic.base import View
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import TemplateView

# Django ORM
from django.db.models import Q
from django.db.models import Max

# Django Exceptions
from django.core.exceptions import PermissionDenied

# Modelos:
from .models import Equipo
from .models import Odometro
from .models import Ubicacion
from .models import Medicion
from .models import UdmOdometro
from .models import TipoOdometro
from home.models import AnexoImagen
from home.models import AnexoArchivo
from home.models import AnexoTexto

# Formularios:
from .forms import EquipoFiltersForm
from .forms import EquipoForm
from .forms import UbicacionForm
from .forms import OdometroForm
from .forms import OdometroFiltersForm
from .forms import MedicionFiltersForm
from .forms import MedicionForm
from .forms import UdmOdometroForm
from .forms import TipoOdometroForm
from .forms import CapturaFiltersForm
from .forms import VerificacionFiltersForm
from home.forms import AnexoTextoForm
from home.forms import AnexoImagenForm
from home.forms import AnexoArchivoForm

# API Rest:
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# API Rest - Serializadores:
from .serializers import EquipoSerializer
from .serializers import EquipoTreeSerilizado
from .serializers import EquipoTreeSerilizado2
from .serializers import UbicacionSerializer
from .serializers import OdometroSerializer
from .serializers import MedicionSerializer
from .serializers import UdmOdometroSerializer
from .serializers import TipoOdometroSerializer
from .serializers import MedicionHistorySerializer
from home.serializers import AnexoTextoSerializer
from home.serializers import AnexoArchivoSerializer
from home.serializers import AnexoImagenSerializer

# API Rest - Paginacion:
from .pagination import GenericPagination

# API Rest - Filtros:
from .filters import EquipoFilter
from .filters import OdometroFilter
from .filters import MedicionFilter
from .filters import EquipoOrdenFilter


# ----------------- EQUIPO ----------------- #

class EquipoListView(View):

    def __init__(self):
        self.template_name = 'equipo/lista.html'

    def get(self, request):

        formulario = EquipoFiltersForm()

        contexto = {
            'form': formulario
        }

        return render(request, self.template_name, contexto)


class EquipoCreateView(View):

    def __init__(self):
        self.template_name = 'equipo/formulario.html'

    def obtener_UrlImagen(self, _imagen):
        imagen = ''

        if _imagen:
            imagen = _imagen.url

        return imagen

    def get(self, request):
        formulario = EquipoForm()
        contexto = {
            'form': formulario,
            'operation': "Nuevo"
        }

        return render(request, self.template_name, contexto)

    def post(self, request):

        url_imagen = ""
        formulario = EquipoForm(request.POST, request.FILES)

        if formulario.is_valid():

            datos_formulario = formulario.cleaned_data
            equipo = Equipo()
            equipo.tag = datos_formulario.get('tag')
            equipo.descripcion = datos_formulario.get('descripcion')
            equipo.serie = datos_formulario.get('serie')
            equipo.especialidad = datos_formulario.get('especialidad')
            equipo.estado = datos_formulario.get('estado')
            equipo.tipo = datos_formulario.get('tipo')
            equipo.padre = datos_formulario.get('padre')
            equipo.empresa = datos_formulario.get('empresa')
            equipo.responsable = datos_formulario.get('responsable')
            equipo.sistema = datos_formulario.get('sistema')
            equipo.ubicacion = datos_formulario.get('ubicacion')
            equipo.imagen = datos_formulario.get('imagen')
            url_imagen = self.obtener_UrlImagen(equipo.imagen)
            equipo.save()

            return redirect(
                reverse('activos:equipos_lista')
            )

        contexto = {
            'form': formulario,
            'imagen': url_imagen,
            'operation': "Nuevo"
        }
        return render(request, self.template_name, contexto)


class EquipoUpdateView(View):

    def __init__(self):
        self.template_name = 'equipo/formulario.html'
        self.tag = ''

    def obtener_UrlImagen(self, _imagen):
        imagen = ''

        if _imagen:
            imagen = _imagen.url

        return imagen

    def get(self, request, pk):

        equipo = get_object_or_404(Equipo, pk=pk)
        self.tag = equipo.tag

        formulario = EquipoForm(
            instance=equipo
        )

        contexto = {
            'form': formulario,
            'tag': self.tag,
            'operation': "Editar",
            'equipo_id': equipo.id,
            'imagen': self.obtener_UrlImagen(equipo.imagen)
        }

        return render(request, self.template_name, contexto)

    def post(self, request, pk):
        if not request.user.is_staff:
            raise PermissionDenied
        else:
            equipo = get_object_or_404(Equipo, pk=pk)
            self.tag = equipo.tag

            formulario = EquipoForm(request.POST, request.FILES, instance=equipo)

            if formulario.is_valid():

                equipo = formulario.save(commit=False)
                equipo.save()

                return redirect(
                    reverse('activos:equipos_lista')
                )

            contexto = {
                'form': formulario,
                'tag': self.tag,
                'operation': "Editar",
                'equipo_id': equipo.id,
                'imagen': self.obtener_UrlImagen(equipo.imagen)
            }
            return render(request, self.template_name, contexto)


class EquipoAPI(viewsets.ModelViewSet):
    queryset = Equipo.objects.all().order_by("-created_date")
    serializer_class = EquipoSerializer
    pagination_class = GenericPagination

    filter_backends = (DjangoFilterBackend,)
    filter_class = EquipoFilter


class EquipoExcelAPI(viewsets.ModelViewSet):
    queryset = Equipo.objects.all().order_by("-created_date")
    serializer_class = EquipoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = EquipoFilter


class EquipoTreeListView(View):

    def __init__(self):
        self.template_name = "equipo/arbol.html"

    def get(self, request, pk):

        equipo = get_object_or_404(Equipo, pk=pk)
        if equipo.estado == "ACT":
            label = "success"
        if equipo.estado == "NOD":
            label = "default"
        if equipo.estado == "DIS":
            label = "disponible"
        if equipo.estado == "REP":
            label = "warning"
        contexto = {
            "equipo": equipo,
            "label": label
        }

        return render(request, self.template_name, contexto)


class EquipoTreeAPI(View):

    def get(self, request, pk):

        daddies = Equipo.objects.filter(pk=pk)

        serializador = EquipoTreeSerilizado()
        lista_json = serializador.get_Json(daddies)

        return HttpResponse(
            lista_json,
            content_type="application/json"
        )


class EquipoTreeAPI2(View):

    def get(self, request, q):

        daddies = Equipo.objects.filter(
            Q(tag__icontains=q) |
            Q(descripcion__icontains=q)
        )

        serializador = EquipoTreeSerilizado2()
        lista_json = serializador.get_Json(daddies)

        return HttpResponse(
            lista_json,
            content_type="application/json"
        )


class EquipoHistory(View):

    def __init__(self):
        self.template_name = 'equipo/historia.html'

    def get(self, request, pk):

        registros = Equipo.history.filter(id=pk).order_by("-history_date")

        contexto = {
            'operation': "Historia",
            'equipo_id': pk,
            'registros': registros
        }

        return render(request, self.template_name, contexto)


class EquipoOrdenAPI(viewsets.ModelViewSet):
    queryset = Equipo.objects.filter(estado="ACT")
    serializer_class = EquipoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = EquipoOrdenFilter


# ----------------- EQUIPO - ANEXO ----------------- #

class AnexoTextoView(View):

    def __init__(self):
        self.template_name = 'equipo/anexos/anexos_texto.html'

    def get(self, request, pk):
        anexos = AnexoTexto.objects.filter(equipo=pk)
        equipo = Equipo.objects.get(id=pk)
        form = AnexoTextoForm()

        contexto = {
            'form': form,
            'id': pk,
            'equipo': equipo,
            'anexos': anexos,
        }

        return render(request, self.template_name, contexto)

    def post(self, request, pk):
        form = AnexoTextoForm(request.POST)
        anexos = AnexoTexto.objects.filter(equipo=pk)
        equipo = Equipo.objects.get(id=pk)

        if form.is_valid():
            texto = form.save(commit=False)
            texto.equipo_id = pk
            texto.save()
            anexos = AnexoTexto.objects.filter(equipo=pk)
            form = AnexoTextoForm()

        contexto = {
            'form': form,
            'id': pk,
            'equipo': equipo,
            'anexos': anexos,
        }
        return render(request, self.template_name, contexto)


class AnexoImagenView(View):

    def __init__(self):
        self.template_name = 'equipo/anexos/anexos_imagen.html'

    def get(self, request, pk):
        anexos = AnexoImagen.objects.filter(equipo=pk)
        equipo = Equipo.objects.get(id=pk)
        form = AnexoImagenForm()

        contexto = {
            'form': form,
            'id': pk,
            'equipo': equipo,
            'anexos': anexos,
        }

        return render(request, self.template_name, contexto)

    def post(self, request, pk):
        anexos = AnexoImagen.objects.filter(equipo=pk)
        equipo = Equipo.objects.get(id=pk)
        form = AnexoImagenForm(request.POST, request.FILES)

        if form.is_valid():

            imagen_anexo = AnexoImagen()
            imagen_anexo.descripcion = request.POST['descripcion']
            if 'ruta' in request.POST:
                imagen_anexo.ruta = request.POST['ruta']
            else:
                imagen_anexo.ruta = request.FILES['ruta']
            imagen_anexo.equipo_id = pk
            imagen_anexo.save()
            form = AnexoImagenForm()
            anexos = AnexoImagen.objects.filter(equipo=pk)

        contexto = {
            'form': form,
            'id': pk,
            'equipo': equipo,
            'anexos': anexos,
        }
        return render(request, self.template_name, contexto)


class AnexoArchivoView(View):

    def __init__(self):
        self.template_name = 'equipo/anexos/anexos_archivo.html'

    def get(self, request, pk):
        anexos = AnexoArchivo.objects.filter(equipo=pk)
        equipo = Equipo.objects.get(id=pk)
        form = AnexoArchivoForm()

        contexto = {
            'form': form,
            'id': pk,
            'equipo': equipo,
            'anexos': anexos,
        }

        return render(request, self.template_name, contexto)

    def post(self, request, pk):
        equipo = Equipo.objects.get(id=pk)
        form = AnexoArchivoForm(request.POST, request.FILES)
        anexos = AnexoArchivo.objects.filter(equipo=pk)

        if form.is_valid():
            archivo_anexo = AnexoArchivo()
            archivo_anexo.descripcion = request.POST['descripcion']
            if 'archivo' in request.POST:
                archivo_anexo.archivo = request.POST['archivo']
            else:
                archivo_anexo.archivo = request.FILES['archivo']
            archivo_anexo.equipo_id = pk
            archivo_anexo.save()
            anexos = AnexoArchivo.objects.filter(equipo=pk)
            form = AnexoArchivoForm()

        contexto = {
            'form': form,
            'id': pk,
            'equipo': equipo,
            'anexos': anexos,
        }

        return render(request, self.template_name, contexto)


class AnexoTextoAPI(viewsets.ModelViewSet):
    queryset = AnexoTexto.objects.all()
    serializer_class = AnexoTextoSerializer
    pagination_class = GenericPagination


class AnexoArchivoAPI(viewsets.ModelViewSet):
    queryset = AnexoArchivo.objects.all()
    serializer_class = AnexoArchivoSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('equipo',)


class AnexoImagenAPI(viewsets.ModelViewSet):
    queryset = AnexoImagen.objects.all()
    serializer_class = AnexoImagenSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('equipo',)


# ----------------- UBICACION ----------------- #

class UbicacionListView(TemplateView):
    template_name = 'ubicacion/lista.html'


class UbicacionCreateView(CreateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = 'ubicacion/formulario.html'
    success_url = reverse_lazy('activos:ubicaciones_lista')
    operation = "Nueva"

    def get_context_data(self, **kwargs):
        contexto = super(UbicacionCreateView, self).get_context_data(**kwargs)
        contexto['operation'] = self.operation
        return contexto


class UbicacionUpdateView(UpdateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = 'ubicacion/formulario.html'
    success_url = reverse_lazy('activos:ubicaciones_lista')
    operation = "Editar"

    def get_context_data(self, **kwargs):
        contexto = super(UbicacionUpdateView, self).get_context_data(**kwargs)
        contexto['operation'] = self.operation
        return contexto


class UbicacionAPI(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('clave', 'descripcion',)


class UbicacionAPI2(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)


# ----------------- ODOMETRO ----------------- #

class OdometroListView(View):
    def __init__(self):
        self.template_name = 'odometro/lista.html'

    def get(self, request):

        formulario = OdometroFiltersForm()

        contexto = {
            'form': formulario
        }

        return render(request, self.template_name, contexto)

    def post(self, request):
        return render(request, self.template_name, {})


class OdometroCreateView(CreateView):
    model = Odometro
    form_class = OdometroForm
    template_name = 'odometro/formulario.html'
    success_url = reverse_lazy('activos:odometros_lista')
    operation = "Nuevo"

    def get_context_data(self, **kwargs):
        contexto = super(OdometroCreateView, self).get_context_data(**kwargs)
        contexto['operation'] = self.operation
        return contexto


class OdometroUpdateView(UpdateView):
    model = Odometro
    form_class = OdometroForm
    template_name = 'odometro/formulario.html'
    success_url = reverse_lazy('activos:odometros_lista')
    operation = "Editar"

    def get_context_data(self, **kwargs):
        contexto = super(OdometroUpdateView, self).get_context_data(**kwargs)
        contexto['operation'] = self.operation
        return contexto


class OdometroAPI(viewsets.ModelViewSet):
    queryset = Odometro.objects.all()
    serializer_class = OdometroSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = OdometroFilter


class OdometroExcelAPI(viewsets.ModelViewSet):
    queryset = Odometro.objects.all()
    serializer_class = OdometroSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = OdometroFilter


# ----------------- UDM ODOMETRO ----------------- #

class UdmOdometroListView(TemplateView):
    template_name = 'udm_odometro/lista.html'


class UdmOdometroCreateView(CreateView):
    model = UdmOdometro
    form_class = UdmOdometroForm
    template_name = 'udm_odometro/formulario.html'
    success_url = reverse_lazy('activos:udms_odometro_lista')
    operation = "Nueva"

    def get_context_data(self, **kwargs):
        contexto = super(
            UdmOdometroCreateView,
            self
        ).get_context_data(**kwargs)
        contexto['operation'] = self.operation
        return contexto


class UdmOdometroUpdateView(UpdateView):
    model = UdmOdometro
    form_class = UdmOdometroForm
    template_name = 'udm_odometro/formulario.html'
    success_url = reverse_lazy('activos:udms_odometro_lista')
    operation = "Editar"

    def get_context_data(self, **kwargs):
        contexto = super(
            UdmOdometroUpdateView,
            self
        ).get_context_data(**kwargs)
        contexto['operation'] = self.operation
        return contexto


class UdmOdometroAPI(viewsets.ModelViewSet):
    queryset = UdmOdometro.objects.all()
    serializer_class = UdmOdometroSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('clave', 'descripcion',)


class UdmOdometroAPI2(viewsets.ModelViewSet):
    queryset = UdmOdometro.objects.all()
    serializer_class = UdmOdometroSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)


# ----------------- MEDICION ----------------- #


class MedicionOdometroView(View):

    def __init__(self):
        self.template_name = 'medicion/lista.html'

    def get(self, request, pk):
        formulario_medicion = MedicionForm()
        id_odometro = pk
        odometro = Odometro.objects.get(id=id_odometro)
        formulario = MedicionFiltersForm()

        contexto = {
            'formulario_medicion': formulario_medicion,
            'form': formulario,
            'id_odometro': id_odometro,
            'odometro': odometro,
        }

        return render(request, self.template_name, contexto)


class MedicionAPI(viewsets.ModelViewSet):
    queryset = Medicion.objects.all().order_by('fecha')
    serializer_class = MedicionSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = MedicionFilter


class MedicionExcelAPI(viewsets.ModelViewSet):
    queryset = Medicion.objects.all().order_by('fecha')
    serializer_class = MedicionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MedicionFilter


class MedicionView(View):

    def __init__(self):
        self.template_name = "medicion/grid.html"

    def crear_NodoEquipo(self, registro):
        nodo_equipo = {}
        nodo_equipo['equipo'] = registro.equipo
        nodo_equipo['id_equipo'] = registro.id_equipo
        nodo_equipo['lista_odometro'] = []
        nodo_odometro = self.crear_NodoOdometro(registro)
        nodo_equipo['lista_odometro'].append(nodo_odometro)

        return nodo_equipo

    def crear_NodoOdometro(self, registro):
        nodo_odometro = {}
        nodo_odometro['id_odometro'] = registro.id_odometro
        nodo_odometro['odometro'] = registro.odometro
        nodo_odometro['descripcion'] = registro.odometro_descripcion
        nodo_odometro['acumulado'] = registro.odometro_acumulado
        nodo_odometro['udm'] = registro.udm
        nodo_odometro['equipo'] = registro.equipo
        nodo_odometro['medicion'] = registro.medicion

        return nodo_odometro

    def get(self, request):

        formulario = MedicionFiltersForm()
        odometros = Odometro.objects.all()
        equipos = Equipo.objects.all()
        equipos_principales = ['PAE_AGOSTO12', 'TREN_1', 'TREN_2', 'TREN_3', 'TREN_4', 'TREN_5']
        resultados = UdmOdometro.objects.raw('''
            select
                1 as id,
                resultados.id_equipo,
                resultados.equipo,
                resultados.id_odometro,
                resultados.odometro,
                resultados.odometro_descripcion,
                resultados.odometro_acumulado,
                resultados.udm as udm,
                CASE resultados.odometro_acumulado
                   WHEN 'ULT' THEN IFNULL((SELECT lectura
                        FROM activos_medicion as med where med.equipo_id = resultados.id_equipo
                        and med.odometro_id = resultados.id_odometro
                        ORDER BY med.fecha DESC
                        LIMIT 1),0)
                   WHEN 'SUM' THEN IFNULL(sum(resultados.lectura), 0)
                END as medicion
                from (
                    select
                        consulta.id_equipo as id_equipo,
                        consulta.equipo as equipo,
                        consulta.id_odometro as id_odometro,
                        consulta.odometro as odometro,
                        consulta.odometro_acumulado as odometro_acumulado,
                        consulta.odometro_descripcion as odometro_descripcion,
                        medicion.lectura as lectura,
                        consulta.udm as udm
                        from
                         (
                             select
                             activos_equipo.tag as equipo,
                             activos_equipo.id as id_equipo,
                             activos_odometro.clave as odometro,
                             activos_odometro.descripcion as odometro_descripcion,
                             activos_odometro.id as id_odometro,
                             activos_odometro.acumulado as odometro_acumulado,
                             udm.descripcion as udm
                             from activos_equipo

                            cross join activos_odometro
                            inner join activos_udmodometro as udm on udm.id = activos_odometro.udm_id
                            where activos_equipo.tag in %s
                        ) as consulta
                        left outer join activos_medicion medicion on medicion.equipo_id = consulta.id_equipo
                              and medicion.odometro_id = consulta.id_odometro
                ) as resultados
                group by resultados.id_equipo,
                resultados.id_odometro
                                    ''', [equipos_principales])

        lista = []
        es_primero = True
        id_anterior = ""
        nodo_equipo = {}
        count = 0
        for r in resultados:
            if r.id_equipo == id_anterior:
                nodo_odometro = self.crear_NodoOdometro(r)
                nodo_equipo['lista_odometro'].append(nodo_odometro)
            else:
                if es_primero:
                    nodo_equipo = self.crear_NodoEquipo(r)
                    es_primero = False
                else:
                    lista.append(nodo_equipo)
                    nodo_equipo = self.crear_NodoEquipo(r)
                id_anterior = r.id_equipo
            count += 1
        if count > 0:
            lista.append(nodo_equipo)

        contexto = {
            'form': formulario,
            'odometros': odometros,
            'equipos': equipos,
            'resultados': lista,
            'equipos_lista': [],
            'odometros_lista': [],
        }

        return render(request, self.template_name, contexto)

    def post(self, request):

        formulario = MedicionFiltersForm(request.POST)
        equipos = request.POST.getlist('equipo')
        odometros = request.POST.getlist('odometro')
        tipo = request.POST.get('tipo')

        equipos_lista = [int(item) for item in equipos]
        odometros_lista = [int(item) for item in odometros]
        equipos_list = json.dumps(equipos_lista)
        odometros_list = json.dumps(odometros_lista)

        boton = ""
        if request.POST.get('buscar'):
            boton = "buscar"
        else:
            boton = "exportar"

        # Se crea lista para enviar al query el parametro tipo
        tipos = []
        if len(equipos) == 0:
            equipos = ['PAE_AGOSTO12', 'TREN_1', 'TREN_2', 'TREN_3', 'TREN_4', 'TREN_5']

        if len(odometros) == 0:
            odometros = []
            l_odometros = Odometro.objects.all()
            for l in l_odometros:
                odometros.append(l.pk)
        # Si no se recibe tipo en el post, se filtra por todos los tipos
        if tipo == '0':
            l_tipo = TipoOdometro.objects.all()
            for l in l_tipo:
                tipos.append(l.pk)

            lista_odometros = Odometro.objects.filter(pk__in=odometros, tipo__in=tipos)
        # Si se recibe un tipo en el post, se hace append a la lista para enviar el parametro
        # y se filtra por ese tipo para enviar el queryset que pintara el header del grid
        else:
            tipo = int(tipo)
            tipos.append(tipo)
            lista_odometros = Odometro.objects.filter(pk__in=odometros, tipo=tipo)

        resultados = UdmOdometro.objects.raw('''
            select
                1 as id,
                resultados.id_equipo,
                resultados.equipo,
                resultados.id_odometro,
                resultados.odometro,
                resultados.odometro_descripcion,
                resultados.odometro_acumulado,
                resultados.udm,
                CASE resultados.odometro_acumulado
                    WHEN 'ULT' THEN IFNULL(
                        (SELECT lectura
                            FROM activos_medicion as med where med.equipo_id = resultados.id_equipo
                                                        and med.odometro_id = resultados.id_odometro
                            ORDER BY med.fecha DESC
                            LIMIT 1),0)
                    WHEN 'SUM' THEN IFNULL(sum(resultados.lectura), 0)
                END as medicion
            from (
                    select
                        consulta.id_equipo as id_equipo,
                        consulta.equipo as equipo,
                        consulta.id_odometro as id_odometro,
                        consulta.odometro as odometro,
                        consulta.odometro_descripcion as odometro_descripcion,
                        consulta.odometro_acumulado as odometro_acumulado,
                        consulta.udm as udm,
                        medicion.lectura as lectura
                    from
                     (
                        select
                        activos_equipo.tag as equipo,
                        activos_equipo.id as id_equipo,
                        activos_odometro.clave as odometro,
                        activos_odometro.descripcion as odometro_descripcion,
                        activos_odometro.acumulado as odometro_acumulado,
                        activos_odometro.id as id_odometro,
                        udm.clave as udm
                        from activos_equipo
                        cross join activos_odometro on activos_odometro.id in %s
                                                    and activos_odometro.tipo_id in %s
                        inner join activos_udmodometro as udm on udm.id = activos_odometro.udm_id
                    ) as consulta
                    left outer join activos_medicion medicion on medicion.equipo_id = consulta.id_equipo
                    and medicion.odometro_id = consulta.id_odometro
                ) as resultados
            where resultados.id_equipo in %s or resultados.equipo in %s
            group by resultados.id_equipo,
            resultados.id_odometro

                            ''', [odometros, tipos, equipos, equipos])

        lista = []
        es_primero = True
        id_anterior = ""
        nodo_equipo = {}
        count = 0
        for r in resultados:
            if r.id_equipo == id_anterior:
                nodo_odometro = self.crear_NodoOdometro(r)
                nodo_equipo['lista_odometro'].append(nodo_odometro)
            else:
                if es_primero:
                    nodo_equipo = self.crear_NodoEquipo(r)
                    es_primero = False
                else:
                    lista.append(nodo_equipo)
                    nodo_equipo = self.crear_NodoEquipo(r)
                id_anterior = r.id_equipo
            count += 1
        if count > 0:
            lista.append(nodo_equipo)
        if boton == 'buscar':
            contexto = {
                'odometros': lista_odometros,
                'form': formulario,
                'resultados': lista,
                'equipos': request.POST.getlist('equipo'),
                'equipos_lista': equipos_list,
                'odometros_lista': odometros_list,
            }
            return render(request, self.template_name, contexto)
        else:
            response = HttpResponse(content_type='application/ms-excel')
            response[
                'Content-Disposition'] = 'attachment; filename="resumen.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet("Resumen", cell_overwrite_ok=True)

            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'dd/mm/yyyy'

            row_num = 0

            font_style = xlwt.XFStyle()

            columns = [
                'Equipo',
            ]
            for o in lista_odometros:
                columns.append(o.descripcion)

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            for row in lista:
                row_num += 1
                col_num = 0
                ws.write(row_num, col_num, row["equipo"], date_format)

                for r in row['lista_odometro']:
                    col_num += 1
                    ws.write(row_num, col_num, r["medicion"], font_style)
                col_num = 0
            wb.save(response)

            return response


class ReporteView(View):

    def __init__(self):
        self.template_name = "medicion/reporte.html"

    def get(self, request):

        formulario = MedicionFiltersForm()

        contexto = {
            'form': formulario,
        }

        return render(request, self.template_name, contexto)

    def post(self, request):
        boton = ''
        if request.POST.get('buscar'):
            boton = 'buscar'
        else:
            boton = 'exportar'
        formulario = MedicionFiltersForm(request.POST)
        lista_equipos = request.POST.getlist('equipo')
        lista_odometros = request.POST.getlist('odometro')
        tipo = request.POST.get('tipo')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        equipos_lista = [int(item) for item in lista_equipos]
        odometros_lista = [int(item) for item in lista_odometros]
        equipos_list = json.dumps(equipos_lista)
        odometros_list = json.dumps(odometros_lista)

        if(len(lista_odometros) == 0):
            odometros = []
            l_odometros = []
            for o in Odometro.objects.all():
                nodo = {}
                nodo["id"] = o.pk
                nodo["descripcion"] = o.descripcion
                nodo["udm"] = o.udm.clave

                l_odometros.append(o.pk)
                odometros.append(nodo)
        else:
            odometros = []
            for o in Odometro.objects.filter(id__in=lista_odometros):
                nodo = {}
                nodo["id"] = o.pk
                nodo["descripcion"] = o.descripcion
                nodo["udm"] = o.udm.clave
                odometros.append(nodo)

            odometros_lista = json.dumps([int(item) for item in lista_odometros])

        if(len(lista_equipos) == 0):
            equipos = []
            l_equipos = []
            for e in Equipo.objects.filter(pk__in=[1, 13, 17]):
                nodo = {}
                nodo["id"] = e.pk
                nodo["tag"] = e.tag
                nodo["descripcion"] = e.descripcion
                equipos.append(nodo)
                l_equipos.append(o.pk)
        else:
            equipos = []
            for e in Equipo.objects.filter(id__in=lista_equipos):
                nodo = {}
                nodo["id"] = e.pk
                nodo["tag"] = e.tag
                nodo["descripcion"] = e.descripcion
                equipos.append(nodo)
        # Si no se recibe tipo en el post, se filtra por todos los tipos
        tipos = []
        if tipo == '0':
            l_tipo = TipoOdometro.objects.all()
            for l in l_tipo:
                tipos.append(l.pk)

            lista_odometros = Odometro.objects.filter(pk__in=lista_odometros, tipo__in=tipos)
        # Si se recibe un tipo en el post, se hace append a la lista para enviar el parametro
        # y se filtra por ese tipo para enviar el queryset que pintara el header del grid
        else:
            tipo = int(tipo)
            tipos.append(tipo)
            lista_odometros = Odometro.objects.filter(pk__in=odometros, tipo=tipo)

        fecha_i = '2017-06-01T00:00:00'
        fecha_f = '2017-06-30T23:59:00'
        # Queryset que trae las mediciones con los filtros
        # resultados = Medicion.objects.filter(
        #     odometro__in=lista_odometros,
        #     equipo__in=equipos,
        #     fecha__gte=fecha_i,
        #     fecha__lte=fecha_f).order_by('-fecha', 'equipo')
        resultados = Medicion.objects.filter(
            fecha__gte=fecha_i,
            fecha__lte=fecha_f).order_by('fecha', 'equipo', 'odometro')
        # Se convierte el queryset a lista
        mediciones = list(resultados)
        lista = []
        if len(mediciones) > 0:
            if boton == "buscar":
                lista_ordenada_fecha = self.crear_lista_ordenada_fecha(mediciones)
                lista_fechas = self.crear_lista_fechas(fecha_inicio, fecha_fin)

                for fecha in lista_fechas:
                    if len(lista_ordenada_fecha) > 0:
                        if fecha < lista_ordenada_fecha[0]["fecha"]:
                            nodo = self.crear_nodo_vacio(fecha, odometros, equipos)
                            lista.append(nodo)
                        elif fecha == lista_ordenada_fecha[0]["fecha"]:
                            self.crear_registro(
                                lista,
                                odometros,
                                equipos,
                                lista_ordenada_fecha[0]["lista_mediciones"],
                                fecha
                            )
                            lista_ordenada_fecha.remove(lista_ordenada_fecha[0])
                            print "el tam de list of ", len(lista_ordenada_fecha)
                    else:
                        nodo = self.crear_nodo_vacio(fecha, odometros, equipos)
                        lista.append(nodo)
        lista2 = lista.sort(reverse=True)
        # print mediciones
        # for l in lista:
        #     print l['fecha']
        #     for x in l['lista_odo']:
        #         print x['lectura'],'  ' ,x['id_equipo'], '  ',x['id_odo']

        contexto = {
            'odometros': lista_odometros,
            'form': formulario,
            'lista': lista2,
            'equipos': request.POST.getlist('equipo'),
            'equipos_lista': equipos_list,
            'odometros_lista': odometros_list,

        }

        return render(request, self.template_name, contexto)

    def crear_lista_fechas(self, fecha_inicio, fecha_fin):
        lista_fechas = []

        f_ini = datetime.datetime.strptime(fecha_inicio, "%m/%d/%Y")
        f_fin = datetime.datetime.strptime(fecha_fin, "%m/%d/%Y")
        while f_ini <= f_fin:

            lista_fechas.append(f_ini)

            f_ini = f_ini + datetime.timedelta(days=1)

        lista_1 = lista_fechas.sort(reverse=True)

        lista_2 = []
        for x in lista_1:
            lista_2.append(x.strftime('%Y-%m-%d'))

        return lista_2

    def crear_nodo_nuevo(self, medicion):
        nodo = {}
        nodo['fecha'] = medicion.fecha.strftime('%m/%d/%Y')
        nodo['lista_mediciones'] = []
        nodo['lista_mediciones'].append(medicion)

        return nodo

    def crear_nodo_vacio(self, fecha, odometros, equipos):
        nodo = {}
        nodo['fecha'] = fecha
        nodo['lista_odo'] = []
        for e in equipos:
            for o in odometros:
                nodo_odo = {}
                nodo_odo["id_odo"] = o["id"]
                nodo_odo['odometro'] = o["descripcion"]
                nodo_odo["lectura"] = 0
                nodo_odo["observaciones"] = ""
                nodo_odo["id_med"] = 0
                nodo_odo['id_equipo'] = e['id']
                nodo_odo['equipo'] = ''
                nodo["lista_odo"].append(nodo_odo)
        return nodo

    def crear_lista_ordenada_fecha(self, mediciones):
        lista = []
        es_primero = True
        count = 0
        for m in mediciones:
            if es_primero:
                nodo = self.crear_nodo_nuevo(m)
                es_primero = False
            else:
                if nodo['fecha'] == m.fecha.strftime('%m/%d/%Y'):
                    nodo['lista_mediciones'].append(m)
                else:
                    lista.append(nodo)
                    nodo = self.crear_nodo_nuevo(m)
            count = count + 1
        if count > 0:
            lista.append(nodo)

        return lista

    def crear_registro(self, lista, odometros, equipos, lista_mediciones, fecha):
        count = 0
        tam_lista = len(lista_mediciones)
        cambios = False

        while tam_lista > 0:
            nodo = {}
            nodo["fecha"] = fecha
            nodo["lista_odo"] = []
            for e in equipos:
                for o in odometros:

                    while count < tam_lista and cambios is not True:
                        if o["id"] == lista_mediciones[count].odometro_id and e['id'] == \
                           lista_mediciones[count].equipo_id:
                            nodo_odo = {}
                            nodo_odo["id_odo"] = o["id"]
                            nodo_odo['odometro'] = o["descripcion"]
                            nodo_odo["lectura"] = lista_mediciones[count].lectura
                            nodo_odo["observaciones"] = lista_mediciones[count].observaciones
                            nodo_odo["id_med"] = lista_mediciones[count].id
                            nodo_odo['id_equipo'] = lista_mediciones[count].equipo_id
                            nodo_odo['equipo'] = lista_mediciones[count].equipo.tag
                            nodo["lista_odo"].append(nodo_odo)
                            lista_mediciones.remove(lista_mediciones[count])
                            tam_lista = len(lista_mediciones)
                            cambios = True
                        count = count + 1
                    if cambios is not True:
                        nodo_odo = {}
                        nodo_odo["id_odo"] = o["id"]
                        nodo_odo['odometro'] = o["descripcion"]
                        nodo_odo["lectura"] = 0
                        nodo_odo["observaciones"] = ""
                        nodo_odo["id_med"] = 0
                        nodo_odo['id_equipo'] = e['id']
                        nodo_odo['equipo'] = ''
                        nodo["lista_odo"].append(nodo_odo)
                    count = 0
                    cambios = False
                lista.append(nodo)


def reporte_mensual(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="seguimiento_operativo.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Integradas por dia', cell_overwrite_ok=True)

    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()

    columns = [
        'Fecha/Hora',
        'Presion de Gas de Entrada',
        'Presion de Gas de Salida',
        'Flujo de Entrada',
        'Flujo de Salida',
        'Diferencia de flujo',
        'Flujo Acumulado de Gas Amargo',
        'Flujo Acumulado de Condensados',
        'Flujo Acum. Gas LP Quemado',
        'Flujo Acum. Gas HP Quemado',
        'Total Quemado',
        'Presion de Gas Combustible',
        'Flujo de Gas Combustible',
        'Cromatografia Gas Combustible',
        'Cromatografia Gas Amargo',
    ]

    row_num += 1
    ws.write_merge(0, 0, 0, 14, 'Fecha')
    row_num += 1
    ws.write_merge(1, 1, 0, 14, 'Reportes Instantaneos del Computador de Flujo')

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Medicion.objects.raw('''
    select
                    resumen.id,
                    STR_TO_DATE(resumen.fechita, %s) as fecha,
                    IFNULL(AVG(resumen.presion_gas_entrada), 0) as presion_gas_entrada,
                    IFNULL(AVG(resumen.presion_gas_salida), 0) as presion_gas_salida,
                    IFNULL(AVG(resumen.flujo_entrada), 0) as flujo_entrada,
                    IFNULL(AVG(resumen.flujo_salida), 0) as flujo_salida,
                    IFNULL(AVG(resumen.flujo_entrada) - AVG(resumen.flujo_salida), 0) as diferencia_flujo,
                    IFNULL(AVG(resumen.flujo_acum_gas_amargo), 0) as flujo_acum_gas_amargo,
                    IFNULL(AVG(resumen.flujo_condensados), 0) as flujo_condensados,
                    IFNULL(AVG(resumen.flujo_lp_quemado), 0) as flujo_lp_quemado,
                    IFNULL(AVG(resumen.flujo_hp_quemado), 0) as flujo_hp_quemado,
                    IFNULL(AVG(resumen.flujo_lp_quemado)  + AVG(resumen.flujo_hp_quemado), 0)as total_quemado,
                    IFNULL(AVG(resumen.presion_gas_combustible), 0) as presion_gas_combustible,
                    IFNULL(AVG(resumen.flujo_gas_combustible), 0) as flujo_gas_combustible,
                    IFNULL(AVG(resumen.crom_gas_combustible), 0) as crom_gas_combustible,
                    IFNULL(AVG(resumen.crom_gas_amargo), 0) as crom_gas_amargo
                from
                (
                    select
                    1 as id,
                    DATE_FORMAT(medicion.fecha, %s) as fechita,
                    (select medicion.lectura where odometro.clave = "PGS") as presion_gas_entrada,
                    (select medicion.lectura where odometro.clave = "PGD") as presion_gas_salida,
                    (select medicion.lectura where odometro.clave = "FDS") as flujo_entrada,
                    (select medicion.lectura where odometro.clave = "FDD") as flujo_salida,
                    (select medicion.lectura where odometro.clave = "FAA") as flujo_acum_gas_amargo,
                    (select medicion.lectura where odometro.clave = "FAC") as flujo_condensados,
                    (select medicion.lectura where odometro.clave = "FGQ") as flujo_lp_quemado,
                    (select medicion.lectura where odometro.clave = "FGA") as flujo_hp_quemado,
                    (select medicion.lectura where odometro.clave = "PGC") as presion_gas_combustible,
                    (select medicion.lectura where odometro.clave = "FGC") as flujo_gas_combustible,
                    (select medicion.lectura where odometro.clave = "CGC") as crom_gas_combustible,
                    (select medicion.lectura where odometro.clave = "CGA") as crom_gas_amargo
                    from activos_medicion as medicion
                    inner join activos_odometro as odometro on odometro.id = medicion.odometro_id
                              where odometro.clave in %s
                        order by fecha asc
                ) resumen
                group by
                    resumen.fechita''', [
        '%d/%m/%Y', '%d/%m/%Y',
        ["PGS", "PGD", "FDS", "FDD", "FAA", "FAC", "FGQ", "FGA", "PGC", "FGC"]
    ]
    )
    daily_rows = Medicion.objects.raw('''
    select
                    resumen.id,
                    resumen.fechita as fecha,
                    IFNULL(AVG(resumen.presion_gas_entrada), 0) as presion_gas_entrada,
                    IFNULL(AVG(resumen.presion_gas_salida), 0) as presion_gas_salida,
                    IFNULL(AVG(resumen.flujo_entrada), 0) as flujo_entrada,
                    IFNULL(AVG(resumen.flujo_salida), 0) as flujo_salida,
                    IFNULL(AVG(resumen.flujo_entrada) - AVG(resumen.flujo_salida), 0) as diferencia_flujo,
                    IFNULL(AVG(resumen.flujo_acum_gas_amargo), 0) as flujo_acum_gas_amargo,
                    IFNULL(AVG(resumen.flujo_condensados), 0) as flujo_condensados,
                    IFNULL(AVG(resumen.flujo_lp_quemado), 0) as flujo_lp_quemado,
                    IFNULL(AVG(resumen.flujo_hp_quemado), 0) as flujo_hp_quemado,
                    IFNULL(AVG(resumen.flujo_lp_quemado)  + AVG(resumen.flujo_hp_quemado), 0)as total_quemado,
                    IFNULL(AVG(resumen.presion_gas_combustible), 0) as presion_gas_combustible,
                    IFNULL(AVG(resumen.flujo_gas_combustible), 0) as flujo_gas_combustible,
                    IFNULL(AVG(resumen.crom_gas_combustible), 0) as crom_gas_combustible,
                    IFNULL(AVG(resumen.crom_gas_amargo), 0) as crom_gas_amargo
                from
                (
                    select
                    1 as id,
                    DATE_FORMAT(medicion.fecha, %s) as fechita,
                    (select medicion.lectura where odometro.clave = "PGS") as presion_gas_entrada,
                    (select medicion.lectura where odometro.clave = "PGD") as presion_gas_salida,
                    (select medicion.lectura where odometro.clave = "FDS") as flujo_entrada,
                    (select medicion.lectura where odometro.clave = "FDD") as flujo_salida,
                    (select medicion.lectura where odometro.clave = "FAA") as flujo_acum_gas_amargo,
                    (select medicion.lectura where odometro.clave = "FAC") as flujo_condensados,
                    (select medicion.lectura where odometro.clave = "FGQ") as flujo_lp_quemado,
                    (select medicion.lectura where odometro.clave = "FGA") as flujo_hp_quemado,
                    (select medicion.lectura where odometro.clave = "PGC") as presion_gas_combustible,
                    (select medicion.lectura where odometro.clave = "FGC") as flujo_gas_combustible,
                    (select medicion.lectura where odometro.clave = "CGC") as crom_gas_combustible,
                    (select medicion.lectura where odometro.clave = "CGA") as crom_gas_amargo
                    from activos_medicion as medicion
                    inner join activos_odometro as odometro on odometro.id = medicion.odometro_id
                        where odometro.clave in ("PGS", "PGD", "FDS", "FDD", "FAA", "FAC", "FGQ", "FGA", "PGC", "FGC")
                                            and medicion.fecha in %s
                        order by fecha asc
                ) resumen
                group by
                    resumen.fechita''', ['%H:%i:%s',
                                         ['2017-06-09 06:00:00', '2017-06-09 07:00:00', '2017-06-09 08:00:00', '2017-06-09 09:00:00', '2017-06-09 10:00:00', ]])
    for row in rows:

        row_num += 1

        ws.write(row_num, 0, row.fecha, date_format)
        ws.write(row_num, 1, row.presion_gas_entrada, font_style)
        ws.write(row_num, 2, row.presion_gas_salida, font_style)
        ws.write(row_num, 3, row.flujo_entrada, font_style)
        ws.write(row_num, 4, row.flujo_salida, font_style)
        ws.write(row_num, 5, row.diferencia_flujo, font_style)
        ws.write(row_num, 6, row.flujo_acum_gas_amargo, font_style)
        ws.write(row_num, 7, row.flujo_condensados, font_style)
        ws.write(row_num, 8, row.flujo_lp_quemado, font_style)
        ws.write(row_num, 9, row.flujo_hp_quemado, font_style)
        ws.write(row_num, 10, row.total_quemado, font_style)
        ws.write(row_num, 11, row.presion_gas_combustible, font_style)
        ws.write(row_num, 12, row.flujo_gas_combustible, font_style)
        ws.write(row_num, 13, row.crom_gas_combustible, font_style)
        ws.write(row_num, 14, row.crom_gas_amargo, font_style)
    # Se agrega la hoja por cada dia del mes
    ws2 = wb.add_sheet('09-06-2016', cell_overwrite_ok=True)

    row_num = 0
    for col_num in range(len(columns)):
        ws2.write(row_num, col_num, columns[col_num], font_style)
    for row in daily_rows:

        row_num += 1

        ws2.write(row_num, 0, row.fecha, date_format)
        ws2.write(row_num, 1, row.presion_gas_entrada, font_style)
        ws2.write(row_num, 2, row.presion_gas_salida, font_style)
        ws2.write(row_num, 3, row.flujo_entrada, font_style)
        ws2.write(row_num, 4, row.flujo_salida, font_style)
        ws2.write(row_num, 5, row.diferencia_flujo, font_style)
        ws2.write(row_num, 6, row.flujo_acum_gas_amargo, font_style)
        ws2.write(row_num, 7, row.flujo_condensados, font_style)
        ws2.write(row_num, 8, row.flujo_lp_quemado, font_style)
        ws2.write(row_num, 9, row.flujo_hp_quemado, font_style)
        ws2.write(row_num, 10, row.total_quemado, font_style)
        ws2.write(row_num, 11, row.presion_gas_combustible, font_style)
        ws2.write(row_num, 12, row.flujo_gas_combustible, font_style)
        ws2.write(row_num, 13, row.crom_gas_combustible, font_style)
        ws2.write(row_num, 14, row.crom_gas_amargo, font_style)

    wb.save(response)

    return response


class CapturaView(View):

    def __init__(self):
        self.template_name = 'medicion/captura.html'

    def get(self, request, equipo=None):
        # Si se recibe el pk del equipo en la url
        if equipo is not None:
            equipo = get_object_or_404(Equipo, pk=equipo)
            id_equipo = equipo.pk
            dia_actual = datetime.datetime.now().day
            mes_actual = datetime.datetime.now().month
            anio_actual = datetime.datetime.now().year

            if dia_actual < 10:
                dia_actual = "0" + str(dia_actual)
            else:
                dia_actual = str(dia_actual)

            if mes_actual < 10:
                mes_actual = "0" + str(mes_actual)
            else:
                mes_actual = str(mes_actual)
            fecha_inicio = str(anio_actual) + "-" + mes_actual + "-" + dia_actual
            fecha_fin = str(anio_actual) + "-" + mes_actual + "-" + dia_actual
            tipo_equipo = equipo.tipo
            if tipo_equipo:
                formulario_medicion = CapturaFiltersForm(
                    initial={
                        'equipo': id_equipo,
                        'tipo_equipo': tipo_equipo.pk,
                        'fecha_inicio': fecha_inicio,
                        'fecha_fin': fecha_fin
                    }
                )
            else:
                formulario_medicion = CapturaFiltersForm(
                    initial={
                        'fecha_inicio': fecha_inicio,
                        'fecha_fin': fecha_fin
                    }
                )
            odometros_lista = []
            odometros = []
            l_odometros = []
            for o in Odometro.objects.all():
                nodo = {}
                nodo["id"] = o.pk
                nodo["descripcion"] = o.descripcion
                nodo["udm"] = o.udm.clave
                nodo["acumulado"] = o.acumulado
                odometros.append(nodo)
                l_odometros.append(o.pk)
            odometros_lista = json.dumps([int(item) for item in l_odometros])
            tipo = []
            for t in TipoOdometro.objects.all():
                tipo.append(t.pk)

            if fecha_inicio == fecha_fin:

                mediciones = Medicion.objects.filter(
                    odometro__in=l_odometros,
                    odometro__tipo__in=tipo,
                    equipo=id_equipo,
                    fecha__contains=fecha_inicio
                ).order_by('-fecha')
            else:
                mediciones = Medicion.objects.filter(
                    odometro__in=l_odometros,
                    odometro__tipo__in=tipo,
                    equipo=id_equipo,
                    fecha__gte=fecha_inicio,
                    fecha__lte=fecha_fin
                ).order_by('-fecha')

            lista = []
            if len(mediciones) > 0:
                    mediciones_lista = list(mediciones)
                    lista_ordenada_fecha = self.crear_lista_ordenada_fecha(mediciones_lista)

                    lista_fechas = self.crea_lista_fechas(fecha_inicio, fecha_fin)
                    lista_fechas.sort(reverse=True)
                    for fecha in lista_fechas:

                        if len(lista_ordenada_fecha) > 0:
                            if fecha > lista_ordenada_fecha[0]["fecha"]:
                                nodo = self.crea_Nodo_vacio(fecha, odometros)
                                lista.append(nodo)
                            elif fecha == lista_ordenada_fecha[0]["fecha"]:
                                self.crea_Registro(lista, odometros, lista_ordenada_fecha[0]["lista_mediciones"], fecha)
                                lista_ordenada_fecha.remove(lista_ordenada_fecha[0])
                        else:
                            nodo = self.crea_Nodo_vacio(fecha, odometros)
                            lista.append(nodo)
                    lista.reverse()
            else:

                lista_fechas = self.crea_lista_fechas(fecha_inicio, fecha_fin)
                for f in lista_fechas:
                    nodo = self.crea_Nodo_vacio(f, odometros)
                    lista.append(nodo)

            contexto = {
                'form': formulario_medicion,
                'equipo': equipo,
                'id_equipo': id_equipo,
                'lista': lista,
                'odometros': odometros,
                'odometros_lista': odometros_lista
            }

            return render(request, self.template_name, contexto)

        else:
            dia_actual = datetime.datetime.now().day
            mes_actual = datetime.datetime.now().month
            anio_actual = datetime.datetime.now().year
            if dia_actual < 10:
                dia_actual = "0" + str(dia_actual)
            else:
                dia_actual = str(dia_actual)

            if mes_actual < 10:
                mes_actual = "0" + str(mes_actual)
            else:
                mes_actual = str(mes_actual)
            fecha_inicio = str(anio_actual) + "-" + mes_actual + "-" + dia_actual
            fecha_fin = str(anio_actual) + "-" + mes_actual + "-" + dia_actual

            formulario_medicion = CapturaFiltersForm(
                initial={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
            )
            contexto = {
                'form': formulario_medicion
            }

            return render(request, self.template_name, contexto)

    def post(self, request, equipo=None):

        boton = ""
        if request.POST.get('buscar') == '':
            boton = "buscar"
        else:
            boton = "exportar"

        formulario = CapturaFiltersForm(request.POST)
        id_equipo = request.POST.get('equipo')
        tipo = int(request.POST.get('tipo'))
        equipo = Equipo.objects.get(pk=id_equipo)
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        lista = []
        odometros_lista = []
        if(tipo == 0):
            odometros = []
            l_odometros = []
            for o in Odometro.objects.all():
                nodo = {}
                nodo["id"] = o.pk
                nodo["descripcion"] = o.descripcion
                nodo["udm"] = o.udm.clave
                nodo["acumulado"] = o.acumulado
                odometros.append(nodo)
                l_odometros.append(o.pk)
            odometros_lista = json.dumps([int(item) for item in l_odometros])
            tipo = []
            for t in TipoOdometro.objects.all():
                tipo.append(t.pk)
        else:
            odometros = []
            l_odometros = []
            for o in Odometro.objects.filter(tipo=tipo):
                nodo = {}
                nodo["id"] = o.pk
                nodo["descripcion"] = o.descripcion
                nodo["udm"] = o.udm.clave
                nodo["acumulado"] = o.acumulado
                odometros.append(nodo)
                l_odometros.append(o.pk)
            odometros_lista = json.dumps([int(item) for item in l_odometros])
            tipo = [tipo]

        if fecha_inicio == fecha_fin:

                mediciones = Medicion.objects.filter(
                    odometro__in=l_odometros,
                    odometro__tipo__in=tipo,
                    equipo=id_equipo,
                    fecha__contains=fecha_inicio
                ).order_by('-fecha')
        else:
            mediciones = Medicion.objects.filter(
                odometro__in=l_odometros,
                odometro__tipo__in=tipo,
                equipo=id_equipo,
                fecha__gte=fecha_inicio,
                fecha__lte=fecha_fin
            ).order_by('-fecha')

        if len(mediciones) > 0:
            if boton == "exportar":
                mediciones_lista = list(mediciones)
                lista_ordenada_fecha = self.crear_lista_ordenada_fecha(mediciones_lista)
                lista_fechas = self.crea_lista_fechas(fecha_inicio, fecha_fin)
                lista_fechas.sort(reverse=True)

                for f in lista_fechas:
                    if len(lista_ordenada_fecha) > 0:
                        if f > lista_ordenada_fecha[0]["fecha"]:
                            nodo = self.crea_Nodo_vacio(f, odometros)
                            lista.append(nodo)
                        elif f == lista_ordenada_fecha[0]["fecha"]:
                            self.crea_Registro(
                                lista, odometros, lista_ordenada_fecha[0]["lista_mediciones"], f)
                            lista_ordenada_fecha.remove(lista_ordenada_fecha[0])
                    else:
                        nodo = self.crea_Nodo_vacio(f, odometros)
                        lista.append(nodo)
                lista.reverse()

                response = HttpResponse(content_type='application/ms-excel')
                response[
                    'Content-Disposition'] = 'attachment; filename="reporte.xls"'

                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet(equipo.tag, cell_overwrite_ok=True)

                date_format = xlwt.XFStyle()
                date_format.num_format_str = 'dd/mm/yyyy'

                row_num = 0

                font_style = xlwt.XFStyle()

                columns = [
                    'Fecha',
                ]
                for o in odometros:
                    columns.append(o["descripcion"])

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)

                for row in lista:
                    row_num += 1
                    col_num = 0
                    ws.write(row_num, col_num, row["fecha"], date_format)

                    for r in row['lista_odo']:
                        col_num += 1

                        ws.write(row_num, col_num, r["lectura"], font_style)
                    col_num = 0
                wb.save(response)

                return response

            elif boton == "buscar":
                mediciones_lista = list(mediciones)

                lista_ordenada_fecha = self.crear_lista_ordenada_fecha(mediciones_lista)

                lista_fechas = self.crea_lista_fechas(fecha_inicio, fecha_fin)
                lista_fechas.sort(reverse=True)
                for f in lista_fechas:

                    if len(lista_ordenada_fecha) > 0:
                        if f > lista_ordenada_fecha[0]["fecha"]:
                            nodo = self.crea_Nodo_vacio(f, odometros)
                            lista.append(nodo)
                        elif f == lista_ordenada_fecha[0]["fecha"]:
                            self.crea_Registro(lista, odometros, lista_ordenada_fecha[0]["lista_mediciones"], f)
                            lista_ordenada_fecha.remove(lista_ordenada_fecha[0])
                    else:
                        nodo = self.crea_Nodo_vacio(f, odometros)
                        lista.append(nodo)
                lista.reverse()
        else:
            lista_fechas = self.crea_lista_fechas(fecha_inicio, fecha_fin)

            for f in lista_fechas:
                nodo = self.crea_Nodo_vacio(f, odometros)
                lista.append(nodo)

        contexto = {
            'form': formulario,
            'equipo': equipo,
            'id_equipo': id_equipo,
            'lista': lista,
            'odometros': odometros,
            'odometros_lista': odometros_lista
        }
        return render(request, self.template_name, contexto)

    def crea_Lista(self, lista_ordenada_fecha, lista_fechas, odometros, id_equipo):
        lista = []
        for f in lista_fechas:
            if len(lista_ordenada_fecha) > 0:
                if f < lista_ordenada_fecha[0]["fecha"]:
                    nodo = self.crea_Nodo_vacio(f, odometros)
                    lista.append(nodo)
                elif f == lista_ordenada_fecha[0]["fecha"]:
                    self.crea_Registro(lista, odometros, lista_ordenada_fecha[0]["lista_mediciones"], f, id_equipo)
                    lista_ordenada_fecha.remove(lista_ordenada_fecha[0])
            else:
                nodo = self.crea_Nodo_vacio(f, odometros)
                lista.append(nodo)
        return lista

    def crea_Registro(self, lista, odometros, lista_mediciones, fecha):
        count = 0
        tam_lista = len(lista_mediciones)
        cambios = False
        nodo = {}
        nodo["fecha"] = fecha
        nodo["lista_odo"] = []
        for o in odometros:
            nodo_odo = {}
            nodo_odo["id_odo"] = o["id"]
            nodo_odo["odometro_descripcion"] = o["descripcion"]
            nodo_odo["odometro_acumulado"] = o["acumulado"]
            nodo_odo["odometro_udm"] = o["udm"]
            nodo_odo["lectura"] = 0

            while count < tam_lista and cambios is not True:
                if o["id"] == lista_mediciones[count].odometro_id:
                    nodo_odo = {}
                    nodo_odo["id_odo"] = o["id"]
                    nodo_odo["odometro_descripcion"] = o["descripcion"]
                    nodo_odo["odometro_acumulado"] = o["acumulado"]
                    nodo_odo["odometro_udm"] = o["udm"]
                    nodo_odo["lectura"] = lista_mediciones[count].lectura
                    nodo["lista_odo"].append(nodo_odo)
                    lista_mediciones.remove(lista_mediciones[count])
                    tam_lista = len(lista_mediciones)
                    cambios = True
                count = count + 1
            if cambios is not True:
                nodo["lista_odo"].append(nodo_odo)
            count = 0
            cambios = False
        lista.append(nodo)

    def crea_Nodo_vacio(self, fecha, odometros):
        nodo = {}
        nodo["fecha"] = fecha
        nodo["lista_odo"] = []
        for o in odometros:
            nodo_odo = {}
            nodo_odo["id_odo"] = o["id"]
            nodo_odo["odometro_descripcion"] = o["descripcion"]
            nodo_odo["odometro_acumulado"] = o["acumulado"]
            nodo_odo["odometro_udm"] = o["udm"]
            nodo_odo["lectura"] = 0
            nodo_odo["id_med"] = 0
            nodo["lista_odo"].append(nodo_odo)
        return nodo

    def crear_lista_ordenada_fecha(self, mediciones):
        lista = []
        es_primero = True
        count = 0
        for m in mediciones:
            if es_primero:
                nodo = self.crea_Nodo_nuevo(m)
                es_primero = False
            else:
                if nodo["fecha"] == m.fecha.strftime("%Y-%m-%d"):
                    nodo["lista_mediciones"].append(m)
                else:
                    lista.append(nodo)
                    nodo = self.crea_Nodo_nuevo(m)
            count += 1
        if count > 0:
            lista.append(nodo)
        return lista

    def crea_lista_fechas(self, fecha_inicio, fecha_fin):
        lista = []
        f_ini = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
        f_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
        while f_ini <= f_fin:
            lista.append(f_ini.strftime("%Y-%m-%d"))
            f_ini = f_ini + datetime.timedelta(days=1)

        return lista

    def crea_Nodo_nuevo(self, medicion):
        nodo = {}
        nodo["fecha"] = medicion.fecha.strftime("%Y-%m-%d")
        nodo["lista_mediciones"] = []
        nodo["lista_mediciones"].append(medicion)
        return nodo

    def crea_Nodo(self, medicion, odometros, lista, equipo):
        nodo = {}
        nodo["fecha"] = medicion.fecha.strftime("20%y-%m-%d %H:%M")
        nodo["id_equipo"] = equipo.pk
        nodo["lista_odo"] = []
        for o in odometros:
            nodo_odo = {}
            nodo_odo["id_odo"] = o["id"]
            nodo_odo["odometro_descripcion"] = o["descripcion"]
            if o["id"] == medicion.odometro_id:
                nodo_odo["id_med"] = medicion.id
                nodo_odo["fecha"] = medicion.fecha.strftime("20%y-%m-%d")
                nodo_odo["hora"] = medicion.fecha.strftime("%H:%M")
                nodo_odo["lectura"] = medicion.lectura
                nodo_odo["observaciones"] = medicion.observaciones
            else:
                nodo_odo["id_med"] = 0
                nodo_odo["fecha"] = "0001-01-01"
                nodo_odo["hora"] = "00:00"
                nodo_odo["lectura"] = '-'
                nodo_odo["observaciones"] = ""
            nodo["lista_odo"].append(nodo_odo)
        lista.append(nodo)

# --------------- TIPO ODOMETRO ----------------- #


class TipoOdometroListView(TemplateView):
    template_name = "tipo_odometro/lista.html"


class TipoOdometroCreateView(CreateView):
    model = TipoOdometro
    form_class = TipoOdometroForm
    template_name = 'tipo_odometro/formulario.html'
    success_url = reverse_lazy('activos:tipo_odometro_lista')
    operation = "Nuevo"

    def get_context_data(self, **kwargs):
        contexto = super(
            TipoOdometroCreateView,
            self
        ).get_context_data(**kwargs)
        contexto['operation'] = self.operation
        return contexto


class TipoOdometroUpdateView(UpdateView):
    model = TipoOdometro
    form_class = TipoOdometroForm
    template_name = 'tipo_odometro/formulario.html'
    success_url = reverse_lazy('activos:tipo_odometro_lista')
    operation = "Editar"

    def get_context_data(self, **kwargs):
        contexto = super(
            TipoOdometroUpdateView,
            self
        ).get_context_data(**kwargs)
        contexto['operation'] = self.operation
        return contexto


class TipoOdometroAPI(viewsets.ModelViewSet):
    queryset = TipoOdometro.objects.all()
    serializer_class = TipoOdometroSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('clave', 'descripcion',)


class CapturaMedicionView(View):

    def __init__(self):
        self.template_name = 'medicion/medicion_captura.html'

    def get(self, request, equipo=None):
        if equipo is not None:
            equipo = get_object_or_404(Equipo, pk=equipo)
            tipo_equipo = equipo.tipo
            formulario = CapturaFiltersForm(
                initial={
                    'tipo_equipo': tipo_equipo.pk,
                    'equipo': equipo.pk,
                }
            )
        else:
            formulario = CapturaFiltersForm()

        contexto = {
            'equipo': equipo,
            'form': formulario
        }

        return render(request, self.template_name, contexto)

    def post(self, request, equipo=None):

        formulario = CapturaFiltersForm(request.POST)
        equipo = request.POST['equipo']
        tipo_odometro = int(request.POST['tipo'])
        horometro = ''
        if tipo_odometro != 0:
            obj_tipo_odometro = TipoOdometro.objects.get(pk=tipo_odometro)
            horometro = obj_tipo_odometro
        obj_equipo = Equipo.objects.get(pk=equipo)
        if tipo_odometro == 0:
            odometros = Odometro.objects.all().exclude(clave='GHT').exclude(clave='CHT')
        else:
            odometros = Odometro.objects.filter(tipo=tipo_odometro).exclude(clave='GHT').exclude(clave='CHT')

        lista_odometros = []
        for o in odometros:
            lista_odometros.append(o.pk)

        ult_fechas_reg = Medicion.objects.values('odometro').annotate(max_fecha=Max('fecha')).order_by()

        mega_query = Q()
        for r in ult_fechas_reg:
            mega_query |= (Q(odometro__exact=r['odometro']) & Q(fecha=r['max_fecha']))

        resultados = Medicion.objects.filter(mega_query).filter(
            equipo=equipo,
            odometro__in=lista_odometros).order_by('odometro', 'fecha')

        lista_mediciones = []
        for resultado in resultados:
            medicion = {}
            medicion['id'] = resultado.pk
            medicion['odometro_pk'] = resultado.odometro.pk
            medicion['odometro'] = resultado.odometro.descripcion
            medicion['odometro_udm'] = resultado.odometro.udm.clave
            medicion['odometro_clasificacion'] = resultado.odometro.clasificacion
            medicion['observaciones'] = resultado.observaciones
            medicion['equipo_pk'] = resultado.equipo.pk
            medicion['fecha'] = resultado.fecha.strftime('%d/%m/%Y %H:%M')
            if resultado.odometro.clasificacion == 'TEX' or resultado.odometro.clasificacion == 'OPC':
                medicion['lectura'] = resultado.observaciones
            if resultado.odometro.clasificacion == 'NUM':
                medicion['lectura'] = resultado.lectura
            lista_mediciones.append(medicion)
        for odometro in odometros:
            r = resultados.filter(odometro=odometro).exists()
            if r is not True:
                medicion = {}
                medicion['id'] = ''
                medicion['odometro_pk'] = odometro.pk
                medicion['odometro'] = odometro.descripcion
                medicion['odometro_udm'] = odometro.udm.clave
                medicion['odometro_clasificacion'] = odometro.clasificacion
                medicion['observaciones'] = "-"
                medicion['equipo_pk'] = obj_equipo.pk
                medicion['fecha'] = ''
                medicion['lectura'] = ''
                lista_mediciones.append(medicion)
        # Aqui se ordena por clasificacion para que comentarios y estado salgan al final
        lista_ctx = sorted(lista_mediciones, key=lambda odometro: odometro['odometro_clasificacion'])

        contexto = {
            'form': formulario,
            'equipo': obj_equipo,
            'odometros': odometros,
            'resultados': lista_ctx,
            'horometro': horometro
        }

        return render(request, self.template_name, contexto)


class MedicionHistorialView(View):
    def __init__(self):
        self.template_name = 'medicion/verificar.html'

    def crea_Registro(self, lista, odometros, lista_mediciones, fecha):
        count = 0
        tam_lista = len(lista_mediciones)
        cambios = False
        while tam_lista > 0:
            nodo = {}
            nodo["fecha"] = fecha
            nodo["lista_odo"] = []
            for o in odometros:
                nodo_odo = {}
                nodo_odo["id_odo"] = o["id"]
                nodo_odo["odometro_descripcion"] = o["descripcion"]
                nodo_odo["odometro_udm"] = o["udm"]
                nodo_odo["lectura"] = 0
                nodo_odo["clasificacion"] = o["clasificacion"]
                nodo_odo["observaciones"] = ""

                while count < tam_lista and cambios is not True:
                    if o["id"] == lista_mediciones[count].odometro_id:
                        nodo_odo = {}
                        nodo_odo["id_odo"] = o["id"]
                        nodo_odo["odometro_descripcion"] = o["descripcion"]
                        nodo_odo["odometro_udm"] = o["udm"]
                        nodo_odo["clasificacion"] = o["clasificacion"]
                        nodo_odo["lectura"] = lista_mediciones[count].lectura
                        nodo_odo["observaciones"] = lista_mediciones[count].observaciones
                        nodo["lista_odo"].append(nodo_odo)
                        lista_mediciones.remove(lista_mediciones[count])
                        tam_lista = len(lista_mediciones)
                        cambios = True
                    count = count + 1
                if cambios is not True:
                    nodo["lista_odo"].append(nodo_odo)
                count = 0
                cambios = False
            lista.append(nodo)

    def crea_Nodo_vacio(self, fecha, odometros):
        nodo = {}
        nodo["fecha"] = fecha
        nodo["lista_odo"] = []
        for o in odometros:
            nodo_odo = {}
            nodo_odo["id_odo"] = o["id"]
            nodo_odo["odometro_descripcion"] = o["descripcion"]
            nodo_odo["odometro_udm"] = o["udm"]
            nodo_odo["clasificacion"] = o["clasificacion"]
            nodo_odo["lectura"] = 0
            nodo_odo["id_med"] = 0
            nodo["lista_odo"].append(nodo_odo)
        return nodo

    def crear_lista_ordenada_fecha(self, mediciones):
        lista = []
        es_primero = True
        count = 0
        for m in mediciones:
            if es_primero:
                nodo = self.crea_Nodo_nuevo(m)
                es_primero = False
            else:
                if nodo["fecha"] == m.fecha.strftime("%Y-%m-%d %H:%M"):
                    nodo["lista_mediciones"].append(m)
                else:
                    lista.append(nodo)
                    nodo = self.crea_Nodo_nuevo(m)
            count += 1
        if count > 0:
            lista.append(nodo)
        return lista

    # Funcion que regresa la lista de fechas de las mediciones encontradas
    def crea_lista_fechas(self, fechas):
        lista = []
        for fecha in fechas:
            lista.append(fecha.strftime("%Y-%m-%d %H:%M"))
            return lista

    def crea_Nodo_nuevo(self, medicion):
        nodo = {}
        nodo["fecha"] = medicion.fecha.strftime("%Y-%m-%d %H:%M")
        nodo["lista_mediciones"] = []
        nodo["lista_mediciones"].append(medicion)
        return nodo

    def crea_Nodo(self, medicion, odometros, lista, equipo):
        nodo = {}
        nodo["fecha"] = medicion.fecha.strftime("20%y-%m-%d %H:%M")
        nodo["id_equipo"] = equipo.pk
        nodo["lista_odo"] = []
        for o in odometros:
            nodo_odo = {}
            nodo_odo["id_odo"] = o["id"]
            nodo_odo["odometro_descripcion"] = o["descripcion"]
            if o["id"] == medicion.odometro_id:
                nodo_odo["id_med"] = medicion.id
                nodo_odo["fecha"] = medicion.fecha.strftime("20%y-%m-%d")
                nodo_odo["hora"] = medicion.fecha.strftime("%H:%M")
                nodo_odo["lectura"] = medicion.lectura
                nodo_odo["observaciones"] = medicion.observaciones
                nodo_odo["clasificacion"] = medicion.odometro.clasificacion
            else:
                nodo_odo["id_med"] = 0
                nodo_odo["fecha"] = "0001-01-01"
                nodo_odo["hora"] = "00:00"
                nodo_odo["lectura"] = '-'
                nodo_odo["observaciones"] = ""
                nodo_odo["clasificacion"] = medicion.odometro.clasificacion
            nodo["lista_odo"].append(nodo_odo)
        lista.append(nodo)

    def get(self, request, equipo, tipo_odometro):

        equipo = Equipo.objects.get(pk=equipo)
        tipo_odometro = TipoOdometro.objects.get(pk=tipo_odometro)
        fecha_hoy = datetime.datetime.today()

        fecha_inicio = fecha_hoy + datetime.timedelta(days=-1)
        fecha_inicio = fecha_hoy.strftime("%Y-%m-%d 05:00")
        fecha_fin = fecha_hoy + datetime.timedelta(days=1)
        fecha_fin = fecha_fin.strftime("%Y-%m-%d 12:00")

        odometros = Odometro.objects.filter(tipo=tipo_odometro)

        formulario = VerificacionFiltersForm(
            initial={
                'tipo_equipo': equipo.tipo.pk,
                'equipo': equipo.pk,
                'tipo': tipo_odometro.pk,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            }
        )

        lista_odometros = []
        for o in odometros:
            lista_odometros.append(o.pk)

        odometros = []
        l_odometros = []
        for o in Odometro.objects.filter(tipo=tipo_odometro.pk):
            nodo = {}
            nodo["id"] = o.pk
            nodo["descripcion"] = o.descripcion
            nodo["udm"] = o.udm.clave
            nodo["clasificacion"] = o.clasificacion
            odometros.append(nodo)
            l_odometros.append(o.pk)

        tipo = []
        for t in TipoOdometro.objects.all():
            tipo.append(t.pk)

        mediciones = Medicion.objects.filter(
            equipo=equipo.pk,
            equipo__tipo=equipo.tipo.pk,
            odometro__tipo=tipo_odometro.pk,
            fecha__gte=fecha_inicio,
            fecha__lte=fecha_fin
        ).order_by('fecha')

        lista = []
        if len(mediciones) > 0:
            mediciones_lista = list(mediciones)
            lista_ordenada_fecha = self.crear_lista_ordenada_fecha(mediciones_lista)
            fechas_list = []
            for m in mediciones:
                fechas_list.append(m.fecha)

            fechas_l = set(fechas_list)
            lista_f = sorted(fechas_l)
            lista_fechas = []
            for f in lista_f:
                lista_fechas.append(datetime.datetime.strftime(f, "%Y-%m-%d %H:%M"))
            for fecha in lista_fechas:
                if len(lista_ordenada_fecha) > 0:
                    if fecha > lista_ordenada_fecha[0]["fecha"]:
                        nodo = self.crea_Nodo_vacio(fecha, odometros)
                        lista.append(nodo)
                    elif fecha == lista_ordenada_fecha[0]["fecha"]:
                        self.crea_Registro(lista, odometros, lista_ordenada_fecha[0]["lista_mediciones"], fecha)
                        lista_ordenada_fecha.remove(lista_ordenada_fecha[0])
                else:
                    nodo = self.crea_Nodo_vacio(fecha, odometros)
                    lista.append(nodo)

        contexto = {
            'equipo': equipo,
            'tipo_odometro': tipo_odometro,
            'form': formulario,
            'odometros': odometros,
            'lista': lista
        }

        return render(request, self.template_name, contexto)

    def post(self, request, equipo, tipo_odometro):
        formulario = VerificacionFiltersForm(request.POST)
        equipo = request.POST['equipo']
        tipo_odometro = request.POST['tipo']
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        equipo = Equipo.objects.get(pk=equipo)
        tipo_odometro = TipoOdometro.objects.get(pk=tipo_odometro)

        odometros = Odometro.objects.filter(tipo=tipo_odometro)

        lista_odometros = []
        for o in odometros:
            lista_odometros.append(o.pk)

        odometros = []
        l_odometros = []
        for o in Odometro.objects.filter(tipo=tipo_odometro.pk):
            nodo = {}
            nodo["id"] = o.pk
            nodo["descripcion"] = o.descripcion
            nodo["udm"] = o.udm.clave
            nodo["clasificacion"] = o.clasificacion
            odometros.append(nodo)
            l_odometros.append(o.pk)
        for o in odometros:
            print "post: ", o["clasificacion"]
        tipo = []
        for t in TipoOdometro.objects.all():
            tipo.append(t.pk)

        mediciones = Medicion.objects.filter(
            equipo=equipo.pk,
            equipo__tipo=equipo.tipo.pk,
            odometro__tipo=tipo_odometro.pk,
            fecha__gte=fecha_inicio,
            fecha__lte=fecha_fin
        ).order_by('fecha')

        lista = []
        if len(mediciones) > 0:
            mediciones_lista = list(mediciones)
            lista_ordenada_fecha = self.crear_lista_ordenada_fecha(mediciones_lista)

            fechas_list = []
            for m in mediciones:
                fechas_list.append(m.fecha)

            fechas_l = set(fechas_list)
            lista_f = sorted(fechas_l)
            lista_fechas = []
            for f in lista_f:
                lista_fechas.append(datetime.datetime.strftime(f, "%Y-%m-%d %H:%M"))
            for fecha in lista_fechas:
                if len(lista_ordenada_fecha) > 0:
                    if fecha > lista_ordenada_fecha[0]["fecha"]:
                        nodo = self.crea_Nodo_vacio(fecha, odometros)
                        lista.append(nodo)
                    elif fecha == lista_ordenada_fecha[0]["fecha"]:
                        self.crea_Registro(lista, odometros, lista_ordenada_fecha[0]["lista_mediciones"], fecha)
                        lista_ordenada_fecha.remove(lista_ordenada_fecha[0])
                else:
                    nodo = self.crea_Nodo_vacio(fecha, odometros)
                    lista.append(nodo)

        contexto = {
            'form': formulario,
            'equipo': equipo,
            'tipo_odometro': tipo_odometro,
            'odometros': odometros,
            'lista': lista
        }
        return render(request, self.template_name, contexto)


class MedicionHistoryAPI(viewsets.ModelViewSet):
    queryset = Medicion.history.all()
    serializer_class = MedicionHistorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'odometro', 'equipo',)

    @list_route(methods=["GET", "POST"])
    def history(self, request):
        mediciones = Medicion.history.all()
        serialized_data = MedicionHistorySerializer(mediciones, many=True)
        return Response(serialized_data.data)


class MedicionHistory(View):

    def __init__(self):
        self.template_name = 'medicion/historial.html'

    def get(self, request, equipo=None, tipo_odometro=None):
        equipo = Equipo.objects.get(pk=equipo)
        formulario = VerificacionFiltersForm(
            initial={
                'equipo': equipo.pk,
                'tipo': tipo_odometro,
                'tipo_equipo': equipo.tipo.pk
            }
        )
        registros = Medicion.history.filter(
            equipo=equipo,
            odometro__tipo=tipo_odometro,
        ).order_by("-history_date")

        # paginator = Paginator(registros, 10)
        # page = request.GET.get('page')
        # try:
        #     registros = paginator.page(page)
        # except PageNotAnInteger:
        #     registros = paginator.page(1)
        # except EmptyPage:
        #     registros = paginator.page(paginator.num_pages)

        contexto = {
            'form': formulario,
            'registros': registros,
            'equipo': equipo,
        }

        return render(request, self.template_name, contexto)

    def post(self, request, equipo=None, tipo_odometro=None):

        formulario = VerificacionFiltersForm(request.POST)
        equipo = request.POST['equipo']
        tipo_odometro = request.POST['tipo']
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        history_type = request.POST['history_type']
        obj_equipo = Equipo.objects.get(pk=equipo)
        registros = Medicion.history.filter(
            equipo=equipo,
            odometro__tipo=tipo_odometro,
            fecha__gte=fecha_inicio,
            fecha__lte=fecha_fin,
            history_type=history_type
        ).order_by("-history_date")
        # paginator = Paginator(registros, 10)
        # page = request.POST.get('page')
        # try:
        #     registros = paginator.page(page)
        # except PageNotAnInteger:
        #     registros = paginator.page(1)
        # except EmptyPage:
        #     registros = paginator.page(paginator.num_pages)
        contexto = {
            'form': formulario,
            'registros': registros,
            'equipo': obj_equipo,
        }

        return render(request, self.template_name, contexto)


def reporte_seguimiento_operativo(request):

    def ajustar_altura_celdas(celda):
        worksheet.set_row(celda, 30)

    # Strings
    texto_descripcion_contrato = "PROVEEDOR: Sistemas Integrales de Compresión, S.A. de C.V. / Tecnologías Relacionadas con Energía y Servicios Especializados S.A. de C.V. /Ardica Construcciones, S.A. de C.V. / Alher Oil & Gas S.A. de C.V. (propuesta conjunta) EL PRESENTE ANEXO ES PARTE INTEGRANTE DEL CONTRATO ARRIBA INDICADO PARA LA EJECUCIÓN  DE: SERVICIO INTEGRAL DE COMPRESIÓN PARA GAS AMARGO CON CAPACIDAD DE 200 MMPCD, INSTALADO EN UNA PLATAFORMA AUTOELEVABLE (JACK UP), PARA INSTALACIONES MARINAS DEL ACTIVO DE PRODUCCIÓN CANTARELL, Y SE FORMULA DE COMÚN ACUERDO ENTRE LAS PARTES EN LOS TÉRMINOS DE LAS CLAUSULAS DE DICHO CONTRATO, PARA HACER CONSTAR QUE LOS SERVICIOS SE LLEVARAN ACABO DE CONFORMIDAD CON EL SIGUIENTE:"
    titulo_mediciones = "MÓDULOS DE COMPRESIÓN DE LA PLATAFORMA AUTO ELEVABLE AGOSTO 12"
    titulo_gas_comb = "PAQUETE ACONDICIONADOR DE GAS COMBUSTIBLE"
    # Logos
    logo_pemex = settings.STATIC_ROOT + '/images/logos/logo_pemex.png'
    logo_nuvoil_trese = settings.STATIC_ROOT + '/images/logos/logo_nuv_trese.png'

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=test.xlsx"
    # Se crea el libro
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    # Estilos de las celdas
    bold = workbook.add_format({'bold': True})
    formato_encabezado = workbook.add_format(
        {
            'align': 'center',
            'valign': 'vcenter'
        }
    )
    formato_datos_documento_left = workbook.add_format(
        {
            'align': 'left',
            'bold': True,
        }
    )
    formato_datos_documento_right = workbook.add_format(
        {
            'align': 'right',
            'bold': True,
        }
    )
    white_centered_cell = workbook.add_format(
        {
            'align': 'center',
            'border': True,
        }
    )
    # Colores hexadecimales del formato
    bg_green = workbook.add_format(
        {
            'bg_color': '#BCEEC3',
            'align': 'center',
            'text_wrap': True,
            'border': True,
        }
    )
    bg_green_negritas = workbook.add_format(
        {
            'bg_color': '#BCEEC3',
            'align': 'center',
            'text_wrap': True,
            'border': True,
            'bold': True,
        }
    )
    bg_blue = workbook.add_format(
        {
            'bg_color': '#0E1A2F',
            'font_color': 'white',
            'align': 'center',
            'border': True,
        }
    )
    bg_orange = workbook.add_format(
        {
            'bg_color': '#FBCCA5',
            'align': 'center',
            'border': True,
        }
    )
    center = workbook.add_format(
        {
            'align': 'center',
            'bg_color': '#FBCCA5',
            'border': True
        }
    )
    superscript = workbook.add_format({'font_script': 1})

    # Se crea la hoja
    worksheet = workbook.add_worksheet('Prueba')
    worksheet.insert_image('A1', logo_pemex)
    # Se hace mas angosta la columna V para que se ajuste al logo de nuvoil-trese
    worksheet.set_column('V:V', 4.8)
    worksheet.insert_image('S1', logo_nuvoil_trese)
    # Encabezado Títulos
    worksheet.merge_range('A1:V1', "", formato_encabezado)
    worksheet.write_rich_string('A1',
                                bold, 'Subdirección de Producción Bloques Aguas Someras AS01',
                                formato_encabezado)
    worksheet.merge_range('A2:V2', "", formato_encabezado)
    worksheet.write_rich_string('A2',
                                bold, 'Administración del Activo Integral de Producción Bloque AS01-01',
                                formato_encabezado)
    worksheet.merge_range('A3:V3', "", formato_encabezado)
    worksheet.write_rich_string('A3',
                                bold, 'Coordinación del Grupo Multidisciplinario de Operación de Pozos e Instalaciones',
                                formato_encabezado)

    # Encabezado datos del documento
    worksheet.merge_range('A6:I6', "", formato_datos_documento_left)
    worksheet.write_rich_string('A6',
                                bold, 'CONTRATO No. 422213801',
                                formato_datos_documento_left)
    worksheet.merge_range('O4:V4', "", formato_datos_documento_right)
    worksheet.write_rich_string('O4',
                                bold, 'ANEXO "11"',
                                formato_datos_documento_right)
    worksheet.merge_range('O5:V5', "", formato_datos_documento_right)
    worksheet.write_rich_string('O5',
                                bold, 'FORMATO DIARIO DE SEGUIMIENTO OPERATIVO',
                                formato_datos_documento_right)
    worksheet.merge_range('O6:V6', "", formato_datos_documento_right)
    worksheet.write_rich_string('O6',
                                bold, 'HOJA 1 DE 1',
                                formato_datos_documento_right)
    worksheet.merge_range('A7:V7', "")
    worksheet.merge_range('A8:V8', "")
    worksheet.merge_range('A9:V9', "")
    format = workbook.add_format()
    format.set_text_wrap()
    format.set_align('justify')
    worksheet.set_row(7, 60)
    worksheet.write('A8', texto_descripcion_contrato, format)
    worksheet.write_rich_string('A10', titulo_mediciones, format)
    worksheet.merge_range('A10:V10', "", bg_green)
    worksheet.write_rich_string('A10', titulo_mediciones, bg_green)
    worksheet.merge_range('A11:I12', "VARIABLES OPERATIVAS", bg_green)
    worksheet.merge_range('J11:V11', "FECHA", bg_green)
    worksheet.write_rich_string('J12', "1", bg_green)
    worksheet.write_rich_string('K12', "2", bg_green)
    worksheet.write_rich_string('L12', "3", bg_green)
    worksheet.write_rich_string('M12', "4", bg_green)
    worksheet.write_rich_string('N12', "5", bg_green)
    # Paquete acondicionador de gas combustible
    worksheet.merge_range('O12:V12', titulo_gas_comb, bg_blue)
    worksheet.set_column('O:O', 20)
    worksheet.write_rich_string('O13', "ESTADO", white_centered_cell)
    worksheet.merge_range('P13:Q13', "T/D/R/M", bg_orange)
    worksheet.merge_range('R13:V13', "", white_centered_cell)
    worksheet.merge_range('O14:Q14', "HORAS DE SERVICIO", bg_green_negritas)

    # Mediciones gas combustible
    worksheet.write_rich_string('O15', "PRESIÓN DE ENTRADA", white_centered_cell)
    worksheet.merge_range('P15:Q15', "", bg_orange)
    worksheet.write_rich_string('P15',
                                'kg/cm',
                                superscript, '2',
                                center
                                )
    worksheet.merge_range('R15:V15', "", white_centered_cell)

    worksheet.write_rich_string('O16', "FLUJO INTEGRADO DE ENTRADA", white_centered_cell)
    worksheet.merge_range('P16:Q16', "MMPCSD", bg_orange)
    worksheet.merge_range('R16:V16', "", white_centered_cell)

    worksheet.write_rich_string('O17', "PRESIÓN DE 1RA REGULACIÓN", white_centered_cell)
    worksheet.merge_range('P17:Q17', "", bg_orange)
    worksheet.write_rich_string('P17',
                                'kg/cm',
                                superscript, '2',
                                center
                                )
    worksheet.merge_range('R17:V17', "", white_centered_cell)

    worksheet.write_rich_string('O18', "PRESIÓN DE 2DA REGULACIÓN", white_centered_cell)
    worksheet.merge_range('P18:Q18', "", bg_orange)
    worksheet.write_rich_string('P18',
                                'kg/cm',
                                superscript, '2',
                                center
                                )
    worksheet.merge_range('R18:V18', "", white_centered_cell)

    worksheet.write_rich_string('O19', "TEMPERATURA DE ENTRADA", white_centered_cell)
    worksheet.merge_range('P19:Q19', "°C", bg_orange)
    worksheet.merge_range('R19:V19', "", white_centered_cell)

    worksheet.write_rich_string('O20', "TEMPERATURA DE SALIDA", white_centered_cell)
    worksheet.merge_range('P20:Q20', "°C", bg_orange)
    worksheet.merge_range('R20:V20', "", white_centered_cell)

    worksheet.write_rich_string('O21', "PRESIÓN DE SALIDA", white_centered_cell)
    worksheet.merge_range('P21:Q21', "", bg_orange)
    worksheet.write_rich_string('P21',
                                'kg/cm',
                                superscript, '2',
                                center
                                )
    worksheet.merge_range('R21:V21', "", white_centered_cell)

    worksheet.merge_range('A13:F13', "ESTADO", white_centered_cell)
    worksheet.merge_range('G13:I13', "T/D/R/M/V", bg_orange)
    # Estados de los trenes de compresion
    worksheet.write('J13', "T", white_centered_cell)
    worksheet.write('K13', "T", white_centered_cell)
    worksheet.write('L13', "T", white_centered_cell)
    worksheet.write('M13', "T", white_centered_cell)
    worksheet.write('N13', "T", white_centered_cell)

    worksheet.merge_range('A14:I14', 'HORAS TRABAJADAS', bg_green)
    # Mediciones de las 5 am
    worksheet.write('J14', "", white_centered_cell)
    worksheet.write('K14', "", white_centered_cell)
    worksheet.write('L14', "", white_centered_cell)
    worksheet.write('M14', "", white_centered_cell)
    worksheet.write('N14', "", white_centered_cell)
    # Horometros
    # List comprehension para hacer mas alta la celda del 15 al 21 (14 - 20)
    [ajustar_altura_celdas(x) for x in range(14, 21)]

    worksheet.merge_range('A15:F15', 'TRAB. CON CARGA \n (T)', bg_green)
    worksheet.merge_range('G15:I15', 'HRS.', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J15', "", white_centered_cell)
    worksheet.write('K15', "", white_centered_cell)
    worksheet.write('L15', "", white_centered_cell)
    worksheet.write('M15', "", white_centered_cell)
    worksheet.write('N15', "", white_centered_cell)

    worksheet.merge_range('A16:F16', 'DISPONIBLE \n (D)', bg_green)
    worksheet.merge_range('G16:I16', 'HRS.', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J16', "", white_centered_cell)
    worksheet.write('K16', "", white_centered_cell)
    worksheet.write('L16', "", white_centered_cell)
    worksheet.write('M16', "", white_centered_cell)
    worksheet.write('N16', "", white_centered_cell)

    worksheet.merge_range('A17:F17', 'REPARACIÓN \n (R)', bg_green)
    worksheet.merge_range('G17:I17', 'HRS.', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J17', "", white_centered_cell)
    worksheet.write('K17', "", white_centered_cell)
    worksheet.write('L17', "", white_centered_cell)
    worksheet.write('M17', "", white_centered_cell)
    worksheet.write('N17', "", white_centered_cell)

    worksheet.merge_range('A18:F18', 'MANTENIMIENTO \n (M)', bg_green)
    worksheet.merge_range('G18:I18', 'HRS.', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J18', "", white_centered_cell)
    worksheet.write('K18', "", white_centered_cell)
    worksheet.write('L18', "", white_centered_cell)
    worksheet.write('M18', "", white_centered_cell)
    worksheet.write('N18', "", white_centered_cell)

    worksheet.merge_range('A19:F19', 'TRAB. EN VACIO \n (V)', bg_green)
    worksheet.merge_range('G19:I19', 'HRS.', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J19', "", white_centered_cell)
    worksheet.write('K19', "", white_centered_cell)
    worksheet.write('L19', "", white_centered_cell)
    worksheet.write('M19', "", white_centered_cell)
    worksheet.write('N19', "", white_centered_cell)

    worksheet.merge_range('A20:F20', 'SIST. DE DETECCIÓN \n DE GAS', bg_green)
    worksheet.merge_range('G20:I20', 'EDO.', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J20', "", white_centered_cell)
    worksheet.write('K20', "", white_centered_cell)
    worksheet.write('L20', "", white_centered_cell)
    worksheet.write('M20', "", white_centered_cell)
    worksheet.write('N20', "", white_centered_cell)

    worksheet.merge_range('A21:F21', 'SIST. DE DETECCIÓN \n DE FUEGO', bg_green)
    worksheet.merge_range('G21:I21', 'EDO.', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J21', "", white_centered_cell)
    worksheet.write('K21', "", white_centered_cell)
    worksheet.write('L21', "", white_centered_cell)
    worksheet.write('M21', "", white_centered_cell)
    worksheet.write('N21', "", white_centered_cell)

    worksheet.merge_range('A22:F22', 'P. SUCCIÓN', bg_green)

    worksheet.merge_range('G22:I22', "", bg_orange)
    worksheet.write_rich_string('G22',
                                'kg/cm',
                                superscript, '2',
                                center
                                )
    # Mediciones de las 5 am
    worksheet.write('J22', "", white_centered_cell)
    worksheet.write('K22', "", white_centered_cell)
    worksheet.write('L22', "", white_centered_cell)
    worksheet.write('M22', "", white_centered_cell)
    worksheet.write('N22', "", white_centered_cell)

    worksheet.merge_range('A23:F23', 'TEMP. SUCCIÓN', bg_green)
    worksheet.merge_range('G23:I23', "", bg_orange)
    worksheet.write_rich_string('G23', '°C', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J23', "", white_centered_cell)
    worksheet.write('K23', "", white_centered_cell)
    worksheet.write('L23', "", white_centered_cell)
    worksheet.write('M23', "", white_centered_cell)
    worksheet.write('N23', "", white_centered_cell)

    worksheet.merge_range('A24:F24', 'PRES. DESC.', bg_green)
    worksheet.merge_range('G24:I24', "", bg_orange)
    worksheet.write_rich_string('G24',
                                'kg/cm',
                                superscript, '2',
                                center
                                )
    # Mediciones de las 5 am
    worksheet.write('J24', "", white_centered_cell)
    worksheet.write('K24', "", white_centered_cell)
    worksheet.write('L24', "", white_centered_cell)
    worksheet.write('M24', "", white_centered_cell)
    worksheet.write('N24', "", white_centered_cell)

    worksheet.merge_range('A25:F25', 'TEMP. DESC.', bg_green)
    worksheet.merge_range('G25:I25', "", bg_orange)
    worksheet.write_rich_string('G25', '°C', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J25', "", white_centered_cell)
    worksheet.write('K25', "", white_centered_cell)
    worksheet.write('L25', "", white_centered_cell)
    worksheet.write('M25', "", white_centered_cell)
    worksheet.write('N25', "", white_centered_cell)

    worksheet.merge_range('A26:F26', 'P.  C.  D. PT8', bg_green)
    worksheet.merge_range('G26:I26', "", bg_orange)
    worksheet.write_rich_string('G26',
                                'kg/cm',
                                superscript, '2',
                                center
                                )
    # Mediciones de las 5 am
    worksheet.write('J26', "", white_centered_cell)
    worksheet.write('K26', "", white_centered_cell)
    worksheet.write('L26', "", white_centered_cell)
    worksheet.write('M26', "", white_centered_cell)
    worksheet.write('N26', "", white_centered_cell)

    worksheet.merge_range('A27:F27', 'T. AVG (T5)', bg_green)
    worksheet.merge_range('G27:I27', "", bg_orange)
    worksheet.write_rich_string('G27', '°C', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J27', "", white_centered_cell)
    worksheet.write('K27', "", white_centered_cell)
    worksheet.write('L27', "", white_centered_cell)
    worksheet.write('M27', "", white_centered_cell)
    worksheet.write('N27', "", white_centered_cell)

    worksheet.merge_range('A28:F28', 'VIBRAC. G. G. \n UD10/11  X/Y', bg_green)
    worksheet.merge_range('G28:I28', "", bg_orange)
    worksheet.write_rich_string('G28', 'um', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J28', "", white_centered_cell)
    worksheet.write('K28', "", white_centered_cell)
    worksheet.write('L28', "", white_centered_cell)
    worksheet.write('M28', "", white_centered_cell)
    worksheet.write('N28', "", white_centered_cell)

    worksheet.merge_range('A29:F29', 'VIBRAC. T. P. \n UD12/13  X/Y', bg_green)
    worksheet.merge_range('G29:I29', "", bg_orange)
    worksheet.write_rich_string('G29', 'um', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J29', "", white_centered_cell)
    worksheet.write('K29', "", white_centered_cell)
    worksheet.write('L29', "", white_centered_cell)
    worksheet.write('M29', "", white_centered_cell)
    worksheet.write('N29', "", white_centered_cell)

    worksheet.merge_range('A30:F30', 'VELOC.  G. G.', bg_green)
    worksheet.merge_range('G30:I30', "", bg_orange)
    worksheet.write_rich_string('G30', 'RPM', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J30', "", white_centered_cell)
    worksheet.write('K30', "", white_centered_cell)
    worksheet.write('L30', "", white_centered_cell)
    worksheet.write('M30', "", white_centered_cell)
    worksheet.write('N30', "", white_centered_cell)

    worksheet.merge_range('A31:F31', 'VELOC. T. P.', bg_green)
    worksheet.merge_range('G31:I31', "", bg_orange)
    worksheet.write_rich_string('G31', 'RPM', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J31', "", white_centered_cell)
    worksheet.write('K31', "", white_centered_cell)
    worksheet.write('L31', "", white_centered_cell)
    worksheet.write('M31', "", white_centered_cell)
    worksheet.write('N31', "", white_centered_cell)

    worksheet.merge_range('A32:F32', 'P. ACEITE LUB G. G.', bg_green)
    worksheet.merge_range('G32:I32', "", bg_orange)
    worksheet.write_rich_string('G32',
                                'kg/cm',
                                superscript, '2',
                                center
                                )
    # Mediciones de las 5 am
    worksheet.write('J32', "", white_centered_cell)
    worksheet.write('K32', "", white_centered_cell)
    worksheet.write('L32', "", white_centered_cell)
    worksheet.write('M32', "", white_centered_cell)
    worksheet.write('N32', "", white_centered_cell)

    worksheet.merge_range('A33:F33', 'HOROMETRO', bg_green)
    worksheet.merge_range('G33:I33', "", bg_orange)
    worksheet.write_rich_string('G33', 'HRS.', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J33', "", white_centered_cell)
    worksheet.write('K33', "", white_centered_cell)
    worksheet.write('L33', "", white_centered_cell)
    worksheet.write('M33', "", white_centered_cell)
    worksheet.write('N33', "", white_centered_cell)

    worksheet.merge_range('A34:F34', 'V. DE REC (% CERRADA).', bg_green)
    worksheet.merge_range('G34:I34', "", bg_orange)
    worksheet.write_rich_string('G34', '% CERRADA.', bg_orange)
    # Mediciones de las 5 am
    worksheet.write('J34', "", white_centered_cell)
    worksheet.write('K34', "", white_centered_cell)
    worksheet.write('L34', "", white_centered_cell)
    worksheet.write('M34', "", white_centered_cell)
    worksheet.write('N34', "", white_centered_cell)

    workbook.close()

    return response
