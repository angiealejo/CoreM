# -*- coding: utf-8 -*-

# Django Atajos:
# import json
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
# from django.core import serializers
from django.db.models import F
from django.db.models import Q


# Django http
# from django.http import HttpResponse
# Django Urls:
from django.core.urlresolvers import reverse

# Django Generic Views
from django.views.generic.base import View

# Django Messages
from django.contrib import messages

# Django exceptions for authentication
from django.core.exceptions import PermissionDenied

# Django template loader
# from django.template.loader import get_template

# Modelos:
from .models import OrdenTrabajo
from .models import Actividad
from .models import ActividadDetalle
from .models import ManoObra
from .models import Material
from .models import ServicioExterno
from .models import SolicitudCompraEncabezado
from .models import SolicitudCompraDetalle

# from seguridad.models import Profile
# Otros Modelos
from home.models import AnexoTexto
from home.models import AnexoImagen
from home.models import AnexoArchivo
from administracion.models import Empresa

# from inventarios.models import Stock
from inventarios.models import Articulo
# from inventarios.models import Almacen

# from activos.models import Equipo

# Otras Librerias:
import xlwt

# Formularios:
from .forms import OrdenTrabajoForm
from .forms import ActividadDetalleForm
from .forms import SolicitudCompraEncabezadoForm

# Otros Formularios
from home.forms import AnexoTextoForm
from home.forms import AnexoImagenForm
from home.forms import AnexoArchivoForm

# API Rest & Json:
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

# Rest Framework APIVIEW
# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

# API Rest - Serializadores:
from .serializers import OrdenTrabajoSerializer
from .serializers import ActividadSerializer

from .serializers import ManoObraSerializer
from .serializers import MaterialSerializer
from .serializers import ServicioExternoSerializer
from .serializers import ActividadDetalleSerializer
from .serializers import SolicitudCompraEncabezadoSerializer
from .serializers import SolicitudCompraDetalleSerializer

from home.serializers import AnexoTextoSerializer
from home.serializers import AnexoImagenSerializer
from home.serializers import AnexoArchivoSerializer

from .business import SolicitudCompraBusiness

# API Rest - Paginacion:
from .pagination import GenericPagination

# API Rest - Filtros:
from .filters import OrdenTrabajoFilter
from .filters import SolicitudCompraEncabezadoFilter

# Formulario Filtros
from .forms import OrdenTrabajoFiltersForm

# from rest_framework.renderers import JSONRenderer
from .forms import SolicitudCompraEncabezadoFiltersForm

# Utilidades
from home.utilities import render_to_pdf


# ----------------- ORDEN DE TRABAJO ----------------- #


class OrdenAbiertaListView(View):

    def __init__(self):
        self.template_name = 'orden_trabajo/lista.html'

    def get(self, _request):
        formulario = OrdenTrabajoFiltersForm()
        contexto = {
            'form': formulario
        }
        return render(_request, self.template_name, contexto)


class OrdenTerminadaListView(View):

    def __init__(self):
        self.template_name = 'orden_trabajo/lista.html'

    def get(self, _request):
        formulario = OrdenTrabajoFiltersForm()
        contexto = {
            'form': formulario
        }
        return render(_request, self.template_name, contexto)


class OrdenTrabajoListView(View):

    def __init__(self):
        self.template_name = 'orden_trabajo/lista.html'

    def get(self, request, estado=None):
        formulario = OrdenTrabajoFiltersForm(initial={'estado': estado})
        contexto = {
            'form': formulario
        }
        return render(request, self.template_name, contexto)


class OrdenTrabajoCreateView(View):

    def __init__(self):
        self.template_name = 'orden_trabajo/formulario.html'

    def get(self, request):
        if not request.user.is_staff:
            raise PermissionDenied
        else:
            formulario = OrdenTrabajoForm(initial={'solicitante': request.user})

            contexto = {
                'form': formulario,
                'operation': "Nueva"
            }

            return render(request, self.template_name, contexto)

    def post(self, request):

        formulario = OrdenTrabajoForm(request.POST)

        if formulario.is_valid():

            datos_formulario = formulario.cleaned_data
            orden = OrdenTrabajo()

            orden.equipo = datos_formulario.get('equipo')
            orden.descripcion = datos_formulario.get('descripcion')
            orden.especialidad = datos_formulario.get('especialidad')
            orden.codigo_reporte = datos_formulario.get('codigo_reporte')
            orden.tipo = datos_formulario.get('tipo')
            orden.estado = datos_formulario.get('estado')
            orden.responsable = datos_formulario.get('responsable')
            orden.solicitante = datos_formulario.get('solicitante')
            orden.permiso = datos_formulario.get('permiso')
            orden.fecha_estimada_inicio = datos_formulario.get(
                'fecha_estimada_inicio'
            )
            orden.fecha_estimada_fin = datos_formulario.get(
                'fecha_estimada_fin'
            )
            orden.fecha_real_inicio = datos_formulario.get('fecha_real_inicio')
            orden.fecha_real_fin = datos_formulario.get('fecha_real_fin')
            orden.observaciones = datos_formulario.get('observaciones')
            orden.motivo_cancelacion = datos_formulario.get('motivo_cancelacion')
            orden.es_template = datos_formulario.get('es_template')

            orden.save()

            return redirect(
                reverse(
                    'trabajos:actividades_lista',
                    kwargs={'pk': orden.id}
                )
            )

        contexto = {
            'form': formulario,
            'operation': "Nueva"
        }

        return render(request, self.template_name, contexto)


class OrdenTrabajoUpdateView(View):

    def __init__(self):
        self.template_name = 'orden_trabajo/formulario.html'

    def get(self, request, pk):

        orden = get_object_or_404(OrdenTrabajo, pk=pk)

        formulario = OrdenTrabajoForm(
            initial={
                'equipo': orden.equipo,
                'descripcion': orden.descripcion,
                'especialidad': orden.especialidad,
                'codigo_reporte': orden.codigo_reporte,
                'tipo': orden.tipo,
                'estado': orden.estado,
                'responsable': orden.responsable,
                'solicitante': orden.solicitante,
                'permiso': orden.permiso,
                'fecha_estimada_inicio': orden.fecha_estimada_inicio,
                'fecha_estimada_fin': orden.fecha_estimada_fin,
                'fecha_real_inicio': orden.fecha_real_inicio,
                'fecha_real_fin': orden.fecha_real_fin,
                'observaciones': orden.observaciones,
                'motivo_cancelacion': orden.motivo_cancelacion,
                'es_template': orden.es_template,
            }
        )

        contexto = {
            'form': formulario,
            'operation': "Editar",
            'orden': orden
        }

        return render(request, self.template_name, contexto)

    def post(self, request, pk):

        formulario = OrdenTrabajoForm(request.POST)

        orden = get_object_or_404(OrdenTrabajo, pk=pk)
        if request.user.is_staff or request.user.profile == orden.responsable:
            if formulario.is_valid():

                datos_formulario = formulario.cleaned_data

                orden.equipo = datos_formulario.get('equipo')
                orden.descripcion = datos_formulario.get('descripcion')
                orden.especialidad = datos_formulario.get('especialidad')
                orden.codigo_reporte = datos_formulario.get('codigo_reporte')
                orden.tipo = datos_formulario.get('tipo')
                orden.estado = datos_formulario.get('estado')
                orden.permiso = datos_formulario.get('permiso')
                orden.responsable = datos_formulario.get('responsable')
                orden.solicitante = datos_formulario.get('solicitante')
                orden.fecha_estimada_inicio = datos_formulario.get(
                    'fecha_estimada_inicio'
                )
                orden.fecha_estimada_fin = datos_formulario.get(
                    'fecha_estimada_fin'
                )
                orden.fecha_real_inicio = datos_formulario.get('fecha_real_inicio')
                orden.fecha_real_fin = datos_formulario.get('fecha_real_fin')
                orden.observaciones = datos_formulario.get('observaciones')
                orden.motivo_cancelacion = datos_formulario.get('motivo_cancelacion')
                orden.es_template = datos_formulario.get('es_template')

                orden.save()

                return redirect(
                    reverse(
                        'trabajos:actividades_lista',
                        kwargs={'pk': orden.id}
                    )
                )

            contexto = {
                'form': formulario,
                'operation': "Editar",
                'orden': orden
            }

            return render(request, self.template_name, contexto)

        else:
            raise PermissionDenied

# ----------------- ORDEN DE TRABAJO - REPORTES ----------------- #


class OrdenTrabajoPreview(View):

    def __init__(self):
        self.template_name = "orden_trabajo/reporte/ordentrabajo_preview.html"

    def obtener_HorasEstimadas(self, _orden):

        horas_estimadas = 0
        actividades = Actividad.objects.filter(orden=_orden)

        for actividad in actividades:

            horas_estimadas += actividad.horas_estimadas

        return horas_estimadas

    def get(self, request, pk):
        orden = OrdenTrabajo.objects.get(pk=pk)

        personal = ManoObra.objects.filter(orden=orden)

        horas_hombre = self.obtener_HorasEstimadas(pk)
        contexto = {
            'orden': orden,
            'operation': 'Imprimir Orden',
            'horas_hombre': horas_hombre,
            'personal': personal,
            # 'subsistema': subsistema,
            # 'subsistema_nivel_uno': subsistema_nivel_uno
        }

        return render(request, self.template_name, contexto)


class ReporteMantenimientoPreview(View):

    def __init__(self):
        self.template_name = "orden_trabajo/reporte/reporte_preview.html"

    def obtener_HorasReales(self, _orden):

        horas_reales = 0
        mano_obra = ManoObra.objects.filter(orden=_orden)

        for persona in mano_obra:

            horas_reales += persona.horas_reales

        return horas_reales

    def obtener_tipoMantenimiento(self, orden):
        tipo_mantenimiento = ""
        if (orden.get_tipo_display() == "PREVENTIVA"):
            tipo_mantenimiento = "PREVENTIVO"
        elif (orden.get_tipo_display() == "PREDICTIVA"):
            tipo_mantenimiento = "PREDICTIVO"
        elif (orden.get_tipo_display() == "CORRECTIVA"):
            tipo_mantenimiento = "CORRECTIVO"
        return tipo_mantenimiento

    def get(self, request, pk):

        orden = OrdenTrabajo.objects.get(pk=pk)
        horas_hombre = self.obtener_HorasReales(pk)

        actividades = Actividad.objects.filter(orden=pk)

        detalles = ActividadDetalle.objects.filter(actividad__orden=pk)

        tipo = self.obtener_tipoMantenimiento(orden)
        personal = ManoObra.objects.filter(orden=orden)
        contexto = {
            'orden': orden,
            'operation': 'Imprimir Reporte',
            'actividades': actividades,
            'horas_hombre': horas_hombre,
            'personal': personal,
            'detalles': detalles,
            'tipo_mantenimiento': tipo
        }

        return render(request, self.template_name, contexto)


class ReporteMantenimientoTestPDF(View):

    def __init__(self):
        self.template_name = "orden_trabajo/reporte/reporte_pdf.html"

    def obtener_HorasReales(self, _orden):

        horas_reales = 0
        mano_obra = ManoObra.objects.filter(orden=_orden)

        for persona in mano_obra:

            horas_reales += persona.horas_reales

        return horas_reales

    def obtener_tipoMantenimiento(self, orden):
        tipo_mantenimiento = ""
        if (orden.get_tipo_display() == "PREVENTIVA"):
            tipo_mantenimiento = "PREVENTIVO"
        elif (orden.get_tipo_display() == "PREDICTIVA"):
            tipo_mantenimiento = "PREDICTIVO"
        elif (orden.get_tipo_display() == "CORRECTIVA"):
            tipo_mantenimiento = "CORRECTIVO"
        return tipo_mantenimiento

    def get(self, request, pk, empresa_pk):

        orden = OrdenTrabajo.objects.get(pk=pk)
        empresa = Empresa.objects.get(pk=empresa_pk)
        horas_hombre = self.obtener_HorasReales(pk)

        actividades = Actividad.objects.filter(orden=pk)
        detalles = ActividadDetalle.objects.filter(actividad__orden=pk)
        tipo = self.obtener_tipoMantenimiento(orden)
        personal = ManoObra.objects.filter(orden=orden)
        contexto = {
            'orden': orden,
            'operation': 'Imprimir Reporte',
            'actividades': actividades,
            'horas_hombre': horas_hombre,
            'personal': personal,
            'detalles': detalles,
            'tipo_mantenimiento': tipo,
            'empresa': empresa
        }

        return render(request, self.template_name, contexto)


class ReporteMantenimientoPDF(View):

    def __init__(self):
        self.template_name = "orden_trabajo/reporte/reporte_pdf.html"

    def obtener_HorasReales(self, _orden):

        horas_reales = 0
        mano_obra = ManoObra.objects.filter(orden=_orden)

        for persona in mano_obra:

            horas_reales += persona.horas_reales

        return horas_reales

    def obtener_tipoMantenimiento(self, orden):
        tipo_mantenimiento = ""
        if (orden.get_tipo_display() == "PREVENTIVA"):
            tipo_mantenimiento = "PREVENTIVO"
        elif (orden.get_tipo_display() == "PREDICTIVA"):
            tipo_mantenimiento = "PREDICTIVO"
        elif (orden.get_tipo_display() == "CORRECTIVA"):
            tipo_mantenimiento = "CORRECTIVO"
        return tipo_mantenimiento

    def get(self, request, pk, empresa_pk):

        orden = OrdenTrabajo.objects.get(pk=pk)
        empresa = Empresa.objects.get(pk=empresa_pk)
        horas_hombre = self.obtener_HorasReales(pk)

        actividades = Actividad.objects.filter(orden=pk)
        detalles = ActividadDetalle.objects.filter(actividad__orden=pk)
        tipo = self.obtener_tipoMantenimiento(orden)
        personal = ManoObra.objects.filter(orden=orden)
        contexto = {
            'orden': orden,
            'operation': 'Imprimir Reporte',
            'actividades': actividades,
            'horas_hombre': horas_hombre,
            'personal': personal,
            'detalles': detalles,
            'tipo_mantenimiento': tipo,
            'empresa': empresa
        }

        pdf = render_to_pdf(
            self.template_name,
            contexto
        )

        if pdf:
            respuesta = HttpResponse(pdf, content_type='application/pdf')
            filename = "reporte_%s.pdf" % ("lista")
            content = "inline; filename='%s'" % (filename)
            respuesta['Content-Disposition'] = content
            return respuesta
        else:
            return HttpResponse("No se pudo generar el PDF")


# ----------------- ORDEN DE TRABAJO - API REST ----------------- #

class OrdenTrabajoAPI(viewsets.ModelViewSet):
    queryset = OrdenTrabajo.objects.all().order_by('-created_date')
    serializer_class = OrdenTrabajoSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = OrdenTrabajoFilter


class OrdenTrabajoExcelAPI(viewsets.ModelViewSet):
    queryset = OrdenTrabajo.objects.all().order_by('-created_date')
    serializer_class = OrdenTrabajoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = OrdenTrabajoFilter


class OrdenTrabajoLastAPI(viewsets.ModelViewSet):
    queryset = OrdenTrabajo.objects.order_by('-created_date')[:10]
    serializer_class = OrdenTrabajoSerializer


class OrdenTrabajoAbiertaAPI(viewsets.ModelViewSet):
    queryset = OrdenTrabajo.objects.filter(estado="CAP").order_by('-created_date')
    serializer_class = OrdenTrabajoSerializer
    pagination_class = GenericPagination


class OrdenTrabajoTerminadaAPI(viewsets.ModelViewSet):
    queryset = OrdenTrabajo.objects.filter(estado="TER").order_by('-created_date')
    serializer_class = OrdenTrabajoSerializer
    pagination_class = GenericPagination


class OrdenTerminadaCountAPI(APIView):

    def get(self, request, format=None):
        total = OrdenTrabajo.objects.filter(estado="TER").count()
        data = {'data': total}
        return Response(data)


class OrdenAbiertaCountAPI(APIView):

    def get(self, request, format=None):
        total = OrdenTrabajo.objects.filter(estado="CAP").count()
        data = {'data': total}
        return Response(data)


# ----------------- ACTIVIDAD ----------------- #


class ActividadListView(View):

    def __init__(self):
        self.template_name = 'actividad/lista.html'

    def get(self, _request, pk):
        permiso = ""
        orden = get_object_or_404(OrdenTrabajo, pk=pk)
        if _request.user.is_staff or _request.user.profile == orden.responsable:
            permiso = "autenticado"
        formulario = OrdenTrabajoForm(
            initial={
                'equipo': orden.equipo,
                'descripcion': orden.descripcion,
                'tipo': orden.tipo,
                'estado': orden.estado,
            }
        )

        formulario.fields['equipo'].widget.attrs['disabled'] = True
        formulario.fields['descripcion'].widget.attrs['disabled'] = True
        formulario.fields['tipo'].widget.attrs['disabled'] = True
        formulario.fields['estado'].widget.attrs['disabled'] = True

        contexto = {
            'form': formulario,
            'orden': orden,
            'permiso': permiso,
        }

        return render(_request, self.template_name, contexto)


class ActividadDetalleView(View):

    def __init__(self):
        self.template_name = 'actividad/evidencia.html'

    def get(self, _request, orden_pk, actividad_pk):
        orden = get_object_or_404(OrdenTrabajo, pk=orden_pk)
        if _request.user.is_staff or _request.user.profile == orden.responsable:
            # Se consulta actividad
            actividad = get_object_or_404(Actividad, pk=actividad_pk)

            # Crear Formulario
            formulario = ActividadDetalleForm()

            # Consultar Detalles
            detalles = actividad.actividaddetalle_set.all()

            contexto = {
                'form': formulario,
                'orden_id': orden_pk,
                'actividad_id': actividad_pk,
                'detalles': detalles
            }

            return render(_request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, _request, orden_pk, actividad_pk):

        # Se inicializa formulario
        formulario = ActividadDetalleForm(
            _request.POST,
            _request.FILES
        )

        # Se consulta actividad
        actividad = get_object_or_404(Actividad, pk=actividad_pk)

        # Validar formulario
        if formulario.is_valid():

            datos_formulario = formulario.cleaned_data

            registro = ActividadDetalle()
            registro.actividad = actividad
            registro.comentarios = datos_formulario.get("comentarios")
            registro.imagen = datos_formulario.get('imagen')
            registro.created_by = _request.user
            registro.save()

            formulario = ActividadDetalleForm()

        # Consultar Detalles de Actividades:
        detalles = actividad.actividaddetalle_set.all()

        contexto = {
            'form': formulario,
            'orden_id': orden_pk,
            'actividad_id': actividad_pk,
            'detalles': detalles
        }
        return render(_request, self.template_name, contexto)


class ActividadDetalleEditarView(View):

    def __init__(self):
        self.template_name = 'actividad/evidencia_detalle.html'

    def get(self, _request, orden_pk, actividad_pk, evidencia_pk):

        # Se obtienen datos de la orden:
        orden = get_object_or_404(OrdenTrabajo, pk=orden_pk)

        # Si el usuario es administrador o responsable de la orden:
        if _request.user.is_staff or _request.user.profile == orden.responsable:

            # Se consulta detalle
            evidencia = get_object_or_404(ActividadDetalle, pk=evidencia_pk)

            # Crear Formulario
            formulario = ActividadDetalleForm(instance=evidencia)

            contexto = {
                'form': formulario,
                'orden_id': evidencia.actividad.orden.pk,
                'actividad_id': evidencia.actividad.pk
            }

            return render(_request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, _request, orden_pk, actividad_pk, evidencia_pk):

        # Se consulta detalle
        evidencia = get_object_or_404(ActividadDetalle, pk=evidencia_pk)

        # Se inicializa formulario
        formulario = ActividadDetalleForm(
            _request.POST,
            _request.FILES,
            instance=evidencia
        )

        if formulario.is_valid():
            formulario.save()

            return redirect(
                reverse(
                    'trabajos:actividad_detalle',
                    kwargs={
                        'orden_pk': evidencia.actividad.orden.pk,
                        'actividad_pk': evidencia.actividad.pk
                    }
                )
            )
        else:
            error = "El formulario no es valido"

        contexto = {
            'mensaje': error,
            'form': formulario
        }

        return render(_request, self.template, contexto)


class ActividadAPI(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('orden', 'id')


class ActividadDetalleAPI(viewsets.ModelViewSet):
    queryset = ActividadDetalle.objects.all()
    serializer_class = ActividadDetalleSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', )


# ----------------- MANO OBRA ----------------- #

class ManoObraListView(View):

    def __init__(self):
        self.template_name = 'mano_obra/lista.html'

    def get(self, _request, pk):
        permiso = ""
        orden = get_object_or_404(OrdenTrabajo, pk=pk)
        if _request.user.is_staff or _request.user.profile == orden.responsable:
            permiso = "autenticado"
        formulario = OrdenTrabajoForm(
            initial={
                'equipo': orden.equipo,
                'descripcion': orden.descripcion,
                'tipo': orden.tipo,
                'estado': orden.estado,
            }
        )

        formulario.fields['equipo'].widget.attrs['disabled'] = True
        formulario.fields['descripcion'].widget.attrs['disabled'] = True
        formulario.fields['tipo'].widget.attrs['disabled'] = True
        formulario.fields['estado'].widget.attrs['disabled'] = True

        contexto = {
            'form': formulario,
            'orden': orden,
            'permiso': permiso,
        }

        return render(_request, self.template_name, contexto)


class ManoObraAPI(viewsets.ModelViewSet):
    queryset = ManoObra.objects.all()
    serializer_class = ManoObraSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('orden', 'id')


# ----------------- MATERIAL ----------------- #

class MaterialListView(View):

    def __init__(self):
        self.template_name = 'material/lista.html'

    def get(self, _request, pk):

        orden = get_object_or_404(OrdenTrabajo, pk=pk)
        permiso = ""
        if _request.user.is_staff or _request.user.profile == orden.responsable:
            permiso = "autenticado"

        formulario = OrdenTrabajoForm(
            initial={
                'equipo': orden.equipo,
                'descripcion': orden.descripcion,
                'tipo': orden.tipo,
                'estado': orden.estado,
            }
        )

        formulario.fields['equipo'].widget.attrs['disabled'] = True
        formulario.fields['descripcion'].widget.attrs['disabled'] = True
        formulario.fields['tipo'].widget.attrs['disabled'] = True
        formulario.fields['estado'].widget.attrs['disabled'] = True

        contexto = {
            'form': formulario,
            'orden': orden,
            'permiso': permiso,
        }

        return render(_request, self.template_name, contexto)


class MaterialAPI(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('orden', 'id')


# ----------------- SERVICIO EXTERNO ----------------- #


class ServicioExternoListView(View):

    def __init__(self):
        self.template_name = 'servicio_externo/lista.html'

    def get(self, _request, pk):

        orden = get_object_or_404(OrdenTrabajo, pk=pk)
        permiso = ""
        if _request.user.is_staff or _request.user.profile == orden.responsable:
            permiso = "autenticado"
        formulario = OrdenTrabajoForm(
            initial={
                'equipo': orden.equipo,
                'descripcion': orden.descripcion,
                'tipo': orden.tipo,
                'estado': orden.estado,
            }
        )

        formulario.fields['equipo'].widget.attrs['disabled'] = True
        formulario.fields['descripcion'].widget.attrs['disabled'] = True
        formulario.fields['tipo'].widget.attrs['disabled'] = True
        formulario.fields['estado'].widget.attrs['disabled'] = True

        contexto = {
            'form': formulario,
            'orden': orden,
            'permiso': permiso,
        }

        return render(_request, self.template_name, contexto)


class ServicioExternoAPI(viewsets.ModelViewSet):
    queryset = ServicioExterno.objects.all()
    serializer_class = ServicioExternoSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('orden', 'id')

# ----------------- ORDEN - ANEXO ----------------- #


class OrdenAnexoTextoView(View):

    def __init__(self):
        self.template_name = 'orden_trabajo/anexos/anexos_texto.html'

    def get(self, request, pk):
        id_orden = pk
        orden_trabajo = OrdenTrabajo.objects.get(id=id_orden)
        if request.user.is_staff or request.user.profile == orden_trabajo.responsable:

            anexos = AnexoTexto.objects.filter(orden_trabajo=id_orden)

            form = AnexoTextoForm()

            contexto = {
                'form': form,
                'id': id_orden,
                'orden_trabajo': orden_trabajo,
                'anexos': anexos,
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        id_orden = pk
        form = AnexoTextoForm(request.POST)
        anexos = AnexoTexto.objects.filter(orden_trabajo=id_orden)
        orden_trabajo = OrdenTrabajo.objects.get(id=id_orden)

        if form.is_valid():
            texto = form.save(commit=False)
            texto.orden_trabajo_id = id_orden
            texto.save()
            anexos = AnexoTexto.objects.filter(orden_trabajo=id_orden)
            form = AnexoTextoForm()
        return render(request, 'orden_trabajo/anexos/anexos_texto.html',
                      {'form': form, 'id': id_orden, 'anexos': anexos,
                       'orden_trabajo': orden_trabajo})


class OrdenAnexoImagenView(View):

    def __init__(self):
        self.template_name = 'orden_trabajo/anexos/anexos_imagen.html'

    def get(self, request, pk):
        id_orden = pk
        orden_trabajo = OrdenTrabajo.objects.get(id=id_orden)
        if request.user.is_staff or request.user.profile == orden_trabajo.responsable:
            anexos = AnexoImagen.objects.filter(orden_trabajo=id_orden)

            form = AnexoImagenForm()

            contexto = {
                'form': form,
                'id': id_orden,
                'orden_trabajo': orden_trabajo,
                'anexos': anexos,
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        id_orden = pk
        anexos = AnexoImagen.objects.filter(orden_trabajo=id_orden)
        orden_trabajo = OrdenTrabajo.objects.get(id=id_orden)
        form = AnexoImagenForm(request.POST, request.FILES)

        if form.is_valid():

            imagen_anexo = AnexoImagen()
            imagen_anexo.descripcion = request.POST['descripcion']
            if 'ruta' in request.POST:
                imagen_anexo.ruta = request.POST['ruta']
            else:
                imagen_anexo.ruta = request.FILES['ruta']
            imagen_anexo.orden_trabajo_id = id_orden
            imagen_anexo.save()
            form = AnexoImagenForm()
            anexos = AnexoImagen.objects.filter(orden_trabajo=id_orden)

        contexto = {
            'form': form,
            'id': id_orden,
            'anexos': anexos,
            'orden_trabajo': orden_trabajo,

        }
        return render(request, self.template_name, contexto)


class OrdenAnexoArchivoView(View):

    def __init__(self):
        self.template_name = 'orden_trabajo/anexos/anexos_archivo.html'

    def get(self, request, pk):
        id_orden = pk
        orden_trabajo = OrdenTrabajo.objects.get(id=id_orden)
        if request.user.is_staff or request.user.profile == orden_trabajo.responsable:
            anexos = AnexoArchivo.objects.filter(orden_trabajo=id_orden)
            form = AnexoArchivoForm()

            contexto = {
                'form': form,
                'id': id_orden,
                'orden_trabajo': orden_trabajo,
                'anexos': anexos,
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        id_orden = pk
        orden_trabajo = OrdenTrabajo.objects.get(id=id_orden)
        form = AnexoArchivoForm(request.POST, request.FILES)
        anexos = AnexoArchivo.objects.filter(orden_trabajo=id_orden)

        if form.is_valid():
            archivo_anexo = AnexoArchivo()
            archivo_anexo.descripcion = request.POST['descripcion']
            if 'archivo' in request.POST:
                archivo_anexo.archivo = request.POST['archivo']
            else:
                archivo_anexo.archivo = request.FILES['archivo']
            archivo_anexo.orden_trabajo_id = id_orden
            archivo_anexo.save()
            anexos = AnexoArchivo.objects.filter(orden_trabajo=id_orden)
            form = AnexoArchivoForm()

        contexto = {
            'form': form,
            'id': id_orden,
            'orden_trabajo': orden_trabajo,
            'anexos': anexos,
        }

        return render(request, self.template_name, contexto)


class OrdenAnexoTextoAPI(viewsets.ModelViewSet):
    queryset = AnexoTexto.objects.all()
    serializer_class = AnexoTextoSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('orden_trabajo',)


class OrdenAnexoImagenAPI(viewsets.ModelViewSet):
    queryset = AnexoImagen.objects.all()
    serializer_class = AnexoImagenSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('orden_trabajo',)


class OrdenAnexoArchivoAPI(viewsets.ModelViewSet):
    queryset = AnexoArchivo.objects.all()
    serializer_class = AnexoArchivoSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('orden_trabajo',)


# ------------- SOLICITUD DE COMPRA ------------------ #


class SolicitudCompraListView(View):

    def __init__(self):
        self.template_name = "requisicion/lista.html"

    def get(self, request):
        formulario = SolicitudCompraEncabezadoFiltersForm()

        contexto = {
            'form': formulario,
            'operation': 'Consulta',
        }

        return render(request, self.template_name, contexto)


class SolicitudCompraCreateView(View):

    def __init__(self):
        self.template_name = "requisicion/formulario.html"
        self.negocio = SolicitudCompraBusiness()

    def get(self, request):
        formulario = SolicitudCompraEncabezadoForm()
        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_encabezado': ''
        }

        return render(request, self.template_name, contexto)

    def post(self, request):

        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(
                SolicitudCompraEncabezado, pk=id_cabecera)
            formulario = SolicitudCompraEncabezadoForm(
                request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraSolicitud(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.validar_LineasDetalle(cabecera)

            if resultado is not True:
                messages.add_message(
                    request,
                    messages.ERROR,
                    resultado
                )

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó solicitud correctamente'
                )
                return redirect(reverse(
                    'trabajos:solicitudes_compra_lista')
                )
        else:

            if id_cabecera:
                cabecera = get_object_or_404(
                    SolicitudCompraEncabezado,
                    pk=id_cabecera
                )
                formulario = SolicitudCompraEncabezadoForm(
                    request.POST, instance=cabecera)
                self.negocio.actualizar_CabeceraSolicitud(
                    cabecera,
                    formulario,
                    request.user.profile
                )

            else:
                formulario = SolicitudCompraEncabezadoForm(request.POST)
                cabecera = self.negocio.crear_CabeceraSolicitud(
                    formulario,
                    request.user.profile,
                )
                if cabecera:

                    id_cabecera = cabecera.pk
                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                        'id_cabecera': id_cabecera,
                        'estado_cabecera': cabecera.get_estado_display()
                    }
                    return render(request, self.template_name, contexto)
                else:

                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                    }
                    return render(request, self.template_name, contexto)

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display()
        }

        return render(request, self.template_name, contexto)


class SolicitudCompraUpdateView(View):

    def __init__(self):
        self.template_name = "requisicion/formulario.html"
        self.negocio = SolicitudCompraBusiness()

    def get(self, request, pk):
        cabecera = get_object_or_404(SolicitudCompraEncabezado, pk=pk)
        formulario = SolicitudCompraEncabezadoForm(instance=cabecera)

        contexto = {
            'form': formulario,
            'operation': 'Editar',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display(),
            'created_date': cabecera.created_date,
            'created_by': cabecera.created_by
        }

        return render(request, self.template_name, contexto)

    def post(self, request, pk):

        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":
            cabecera = get_object_or_404(
                SolicitudCompraEncabezado, pk=id_cabecera)
            formulario = SolicitudCompraEncabezadoForm(
                request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraSolicitud(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.validar_LineasDetalle(cabecera)

            if resultado is not True:
                messages.add_message(
                    request,
                    messages.ERROR,
                    resultado
                )

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó solicitud correctamente'
                )
                return redirect(reverse(
                    'trabajos:solicitudes_compra_lista')
                )
        else:

            # Actualiza el encabezado
            cabecera = get_object_or_404(
                SolicitudCompraEncabezado,
                pk=id_cabecera
            )
            formulario = SolicitudCompraEncabezadoForm(
                request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraSolicitud(
                cabecera,
                formulario,
                request.user.profile
            )

        contexto = {
            'form': formulario,
            'operation': 'Editar',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display()
        }

        return render(request, self.template_name, contexto)


class SolicitudCompraEncabezadoAPI(viewsets.ModelViewSet):
    queryset = SolicitudCompraEncabezado.objects.all()
    serializer_class = SolicitudCompraEncabezadoSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = SolicitudCompraEncabezadoFilter


class SolicitudCompraEncabezadoExcelAPI(viewsets.ModelViewSet):
    queryset = SolicitudCompraEncabezado.objects.all()
    serializer_class = SolicitudCompraEncabezadoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = SolicitudCompraEncabezadoFilter


class SolicitudCompraDetalleAPI(viewsets.ModelViewSet):
    queryset = SolicitudCompraDetalle.objects.all()
    serializer_class = SolicitudCompraDetalleSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('encabezado',)


class SolicitudCompraDetalleExcelAPI(viewsets.ModelViewSet):
    queryset = SolicitudCompraDetalle.objects.all()
    serializer_class = SolicitudCompraDetalleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('encabezado',)

# ------------- NECESIDADES ------------------ #


class NecesidadesView(View):

    def __init__(self):
        self.template_name = "requisicion/necesidades.html"

    def get(self, request):

        necesidades_stock = Articulo.objects.filter(
            Q(stock__almacen__descripcion__icontains="AGOSTO", stock__cantidad__lt=F("stock_seguridad")) |
            Q(stock__isnull=True)
        ).exclude(stock_seguridad__exact=0)

        necesidades_ot = Articulo.objects.raw('''
            select
                resumen.articulo_id as id,
                resumen.sum_cantidad_estimada,
                resumen.sum_cantidad_estimada - resumen.sum_cantidad_real - IFNULL(stock.cantidad,0) as faltante
            from (
                    select
                    ot_mat.articulo_id,
                    sum(ot_mat.cantidad_estimada) as sum_cantidad_estimada,
                    sum(ot_mat.cantidad_real) as sum_cantidad_real
                    from trabajos_material ot_mat
                    left outer join trabajos_ordentrabajo ot on 1=1
                                and ot.id = ot_mat.orden_id
                    where 1=1
                    and ot.estado in ('CAP')
                    group by
                        ot_mat.articulo_id
                 ) resumen
            left outer join inventarios_stock stock on 1=1
                        and stock.articulo_id = resumen.articulo_id
                        and stock.almacen_id = '2'
            left outer join inventarios_almacen alm on 1=1
                        and alm.id = stock.almacen_id
                        and alm.descripcion like %s
            where 1=1
            and (resumen.sum_cantidad_estimada - resumen.sum_cantidad_real) > IFNULL(stock.cantidad,0)''', ["agosto"])

        count_records = len(list(necesidades_ot))

        if count_records == 0:
            necesidades_ot = None

        contexto = {
            'necesidades_stock': necesidades_stock,
            'necesidades_ot': necesidades_ot
        }

        return render(request, self.template_name, contexto)


class NecesidadesDetalleView(View):

    def __init__(self):
        self.template_name = "requisicion/necesidades_detalle.html"

    def get(self, request, pk):

        material = Material.objects.filter(
            orden__estado__in=["CAP"],
            articulo__pk=pk
        )

        contexto = {
            'material': material
        }

        return render(request, self.template_name, contexto)


def export_nec_stock_seguridad(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="req_stock_seguridad.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('StockSeguridad')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()

    columns = [
        'Clave',
        'Descripcion',
        'UDM',
        'Tipo',
        'Clave JDE',
        'URL',
        'Marca',
        'Modelo',
        'No. Parte',
        'Stock Maximo',
        'Stock Minimo',
        'Stock Seguridad',
        'Cantidad Actual',
        'Faltan'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Articulo.objects.filter(
        Q(stock__almacen__descripcion__icontains="AGOSTO", stock__cantidad__lte=F("stock_seguridad")) |
        Q(stock__isnull=True)
    ).exclude(stock_seguridad__exact=0)

    for row in rows:
        row_num += 1

        ws.write(row_num, 0, row.clave, font_style)
        ws.write(row_num, 1, row.descripcion, font_style)
        ws.write(row_num, 2, row.udm.clave, font_style)
        ws.write(row_num, 3, row.get_tipo_display(), font_style)
        ws.write(row_num, 4, row.clave_jde, font_style)
        ws.write(row_num, 5, row.url, font_style)
        ws.write(row_num, 6, row.marca, font_style)
        ws.write(row_num, 7, row.modelo, font_style)
        ws.write(row_num, 8, row.numero_parte, font_style)
        ws.write(row_num, 9, row.stock_maximo, font_style)
        ws.write(row_num, 10, row.stock_minimo, font_style)
        ws.write(row_num, 11, row.stock_seguridad, font_style)
        ws.write(row_num, 12, row.cantidad_stock, font_style)
        ws.write(row_num, 13, row.faltantes_stock_seguridad, font_style)

    wb.save(response)
    return response


def export_nec_ot(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="req_stock_seguridad.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('OrdenNecesidad')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()

    columns = [
        'Clave',
        'Descripcion',
        'UDM',
        'Tipo',
        'Clave JDE',
        'URL',
        'Marca',
        'Modelo',
        'No. Parte',
        'Stock Maximo',
        'Stock Minimo',
        'Stock Seguridad',
        'Cantidad Actual',
        'Faltan'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Articulo.objects.raw('''
            select
                resumen.articulo_id as id,
                resumen.sum_cantidad_estimada,
                resumen.sum_cantidad_estimada - resumen.sum_cantidad_real - IFNULL(stock.cantidad,0) as faltante
            from (
                    select
                    ot_mat.articulo_id,
                    sum(ot_mat.cantidad_estimada) as sum_cantidad_estimada,
                    sum(ot_mat.cantidad_real) as sum_cantidad_real
                    from trabajos_material ot_mat
                    left outer join trabajos_ordentrabajo ot on 1=1
                                and ot.id = ot_mat.orden_id
                    where 1=1
                    and ot.estado in ('CAP')
                    group by
                        ot_mat.articulo_id
                 ) resumen
            left outer join inventarios_stock stock on 1=1
                        and stock.articulo_id = resumen.articulo_id
                        and stock.almacen_id = '2'
            left outer join inventarios_almacen alm on 1=1
                        and alm.id = stock.almacen_id
                        and alm.descripcion like %s
            where 1=1
            and (resumen.sum_cantidad_estimada - resumen.sum_cantidad_real) > IFNULL(stock.cantidad,0)''', ["agosto"])

    for row in rows:
        row_num += 1

        ws.write(row_num, 0, row.clave, font_style)
        ws.write(row_num, 1, row.descripcion, font_style)
        ws.write(row_num, 2, row.udm.clave, font_style)
        ws.write(row_num, 3, row.get_tipo_display(), font_style)
        ws.write(row_num, 4, row.clave_jde, font_style)
        ws.write(row_num, 5, row.url, font_style)
        ws.write(row_num, 6, row.marca, font_style)
        ws.write(row_num, 7, row.modelo, font_style)
        ws.write(row_num, 8, row.numero_parte, font_style)
        ws.write(row_num, 9, row.stock_maximo, font_style)
        ws.write(row_num, 10, row.stock_minimo, font_style)
        ws.write(row_num, 11, row.stock_seguridad, font_style)
        ws.write(row_num, 12, row.cantidad_stock, font_style)
        ws.write(row_num, 13, row.faltante, font_style)
        # for col_num in range(len(row)):

    wb.save(response)
    return response
