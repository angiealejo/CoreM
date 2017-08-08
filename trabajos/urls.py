# -*- coding: utf-8 -*-

# Librerias Django:
from django.conf.urls import url

# Autenticacion
# from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

# Vistas:
from .views import OrdenTrabajoListView
from .views import OrdenTrabajoCreateView
from .views import OrdenTrabajoUpdateView

from .views import ActividadListView
from .views import ActividadDetalleView
from .views import ActividadDetalleEditarView
from .views import MaterialListView
from .views import ManoObraListView
from .views import ServicioExternoListView
from .views import OrdenAbiertaListView
from .views import OrdenTerminadaListView
from .views import OrdenTrabajoPreview
from .views import ReporteMantenimientoPreview
from .views import ReporteMantenimientoTestPDF
from .views import ReporteMantenimientoPDF
from .views import SolicitudCompraCreateView
from .views import SolicitudCompraListView
from .views import SolicitudCompraUpdateView

from .views import OrdenTerminadaCountAPI
from .views import OrdenAbiertaCountAPI

from .views import OrdenAnexoTextoView
from .views import OrdenAnexoImagenView
from .views import OrdenAnexoArchivoView

from .views import NecesidadesView
from .views import NecesidadesDetalleView
from .views import export_nec_stock_seguridad
from .views import export_nec_ot

app_name = 'trabajos'

urlpatterns = [

    # ----------------- ORDEN DE TRABAJO ----------------- #
    url(
        r'^ordenes/busqueda/(?P<estado>\w+)/$',
        login_required(OrdenTrabajoListView.as_view()),
        name='ordenes_lista_estado'
    ),
    url(
        r'^ordenes/$',
        login_required(OrdenTrabajoListView.as_view()),
        name='ordenes_lista'
    ),
    url(
        r'^ordenes/abiertas/$',
        login_required(OrdenAbiertaListView.as_view()),
        name='ordenes_abiertas'
    ),
    url(
        r'^ordenes/terminadas/$',
        login_required(OrdenTerminadaListView.as_view()),
        name='ordenes_terminadas'
    ),
    url(
        r'^ordenes/nuevo/$',
        login_required(OrdenTrabajoCreateView.as_view()),
        name='ordenes_nueva'
    ),
    url(
        r'^ordenes/editar/(?P<pk>.*)/$',
        login_required(OrdenTrabajoUpdateView.as_view()),
        name='ordenes_editar'
    ),
    url(
        r'^ordenestrabajoterminadas/$',
        login_required(OrdenTerminadaCountAPI.as_view()),
        name='ordenes_terminadas_count'
    ),
    url(
        r'^ordenestrabajoabiertas/$',
        login_required(OrdenAbiertaCountAPI.as_view()),
        name='ordenes_abiertas_count'
    ),

    # ----------------- ORDEN DE TRABAJO - REPORTES ----------------- #

    url(
        r'^ordenes/preview/(?P<pk>.*)/$',
        login_required(OrdenTrabajoPreview.as_view()),
        name='ordenes_preview'
    ),
    url(
        r'^ordenes/reporte/preview/(?P<pk>.*)/$',
        login_required(ReporteMantenimientoPreview.as_view()),
        name='ordenes_reporte_preview'
    ),

    url(
        r'^ordenes/reporte/pdftest/(?P<pk>.*)/empresa/(?P<empresa_pk>.*)/$',
        login_required(ReporteMantenimientoTestPDF.as_view()),
        name='ordenes_reporte_prueba_pdf'
    ),
    url(
        r'^ordenes/reporte/pdf/(?P<pk>.*)/empresa/(?P<empresa_pk>.*)/$',
        login_required(ReporteMantenimientoPDF.as_view()),
        name='ordenes_reporte_pdf'
    ),

    # ----------------- ACTIVIDADES ----------------- #

    url(
        r'^ordenes/(?P<pk>.*)/actividades/$',
        login_required(ActividadListView.as_view()),
        name='actividades_lista'
    ),

    url(
        r'^ordenes/(?P<orden_pk>.*)/actividades/(?P<actividad_pk>.*)/detalle/$',
        login_required(ActividadDetalleView.as_view()),
        name='actividad_detalle'
    ),

    url(
        r'^ordenes/(?P<orden_pk>.*)/actividades/(?P<actividad_pk>.*)/detalle/(?P<evidencia_pk>.*)/$',
        login_required(ActividadDetalleEditarView.as_view()),
        name='actividad_detalle_editar'
    ),

    # ----------------- MATERIAL ----------------- #

    url(
        r'^ordenes/(?P<pk>.*)/materiales/$',
        login_required(MaterialListView.as_view()),
        name='material_lista'
    ),

    # ----------------- MANO OBRA ----------------- #

    url(
        r'^ordenes/(?P<pk>.*)/mano_obra/$',
        login_required(ManoObraListView.as_view()),
        name='mano_obra_lista'
    ),

    # ----------------- SERVICIO EXTERNO ----------------- #

    url(
        r'^ordenes/(?P<pk>.*)/servicios/$',
        login_required(ServicioExternoListView.as_view()),
        name='servicio_externo_lista'
    ),

    # ----------------- ORDENES - ANEXOS ----------------- #
    url(
        r'ordenes/anexos/(?P<pk>\d+)/texto/$',
        login_required(OrdenAnexoTextoView.as_view()),
        name='orden_anexar_texto'
    ),
    url(
        r'^ordenes/anexos/(?P<pk>\d+)/imagen/$',
        login_required(OrdenAnexoImagenView.as_view()),
        name='orden_anexar_imagen'
    ),
    url(
        r'^ordenes/anexos/(?P<pk>\d+)/archivo/$',
        login_required(OrdenAnexoArchivoView.as_view()),
        name='orden_anexar_archivo'
    ),

    # -------- SOLICITUD COMPRA ---------------- #
    url(
        r'solicitudes_compra/$',
        login_required(SolicitudCompraListView.as_view()),
        name='solicitudes_compra_lista'
    ),
    url(
        r'solicitudes_compra/nuevo/$',
        login_required(SolicitudCompraCreateView.as_view()),
        name='solicitudes_compra_nuevo'
    ),
    url(
        r'solicitudes_compra/editar/(?P<pk>\d+)/$',
        login_required(SolicitudCompraUpdateView.as_view()),
        name='solicitudes_compra_editar'
    ),

    # -------- NECESIDADES ---------------- #

    url(
        r'necesidades/$',
        NecesidadesView.as_view(),
        name='necesidades'
    ),
    url(
        r'necesidades/detalle/(?P<pk>\d+)/$',
        NecesidadesDetalleView.as_view(),
        name='necesidades_detalle'
    ),
    url(
        r'^necesidades/stock_seguridad/$',
        export_nec_stock_seguridad,
        name='necesidades_stock_seg'
    ),
    url(
        r'^necesidades/ot/$',
        export_nec_ot,
        name='necesidades_ot'
    ),
]
