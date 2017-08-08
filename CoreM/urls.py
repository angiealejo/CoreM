# -*- coding: utf-8 -*-

# Librerias django
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

# API Rest
from rest_framework import routers

# API Rest - Views:
from activos.views import EquipoAPI
from activos.views import UbicacionAPI
from activos.views import UbicacionAPI2
from activos.views import AnexoTextoAPI
from activos.views import AnexoArchivoAPI
from activos.views import AnexoImagenAPI
from activos.views import OdometroAPI
from activos.views import OdometroExcelAPI
from activos.views import UdmOdometroAPI
from activos.views import UdmOdometroAPI2
from activos.views import MedicionAPI
from activos.views import MedicionExcelAPI
from activos.views import EquipoOrdenAPI
from activos.views import EquipoExcelAPI
from activos.views import TipoOdometroAPI
from inventarios.views import AlmacenAPI
from inventarios.views import AlmacenAPI2
from inventarios.views import UdmArticuloAPI
from inventarios.views import UdmArticuloAPI2
from inventarios.views import ArticuloAPI
from inventarios.views import ArticuloAPI2
from inventarios.views import ArticuloForOrdenesAPI
from inventarios.views import ArticuloForPersonalAPI
from inventarios.views import ArticuloAnexoTextoAPI
from inventarios.views import ArticuloAnexoImagenAPI
from inventarios.views import ArticuloAnexoArchivoAPI
from inventarios.views import StockAPI
from inventarios.views import StockExcelAPI
from inventarios.views import MovimientoAPI
from inventarios.views import MovimientoExcelAPI
from inventarios.views import MovimientoDetalleAPI
from inventarios.views import MovimientoDetalleExcelAPI
from inventarios.views import MovimientoInventarioAPI
from inventarios.views import MovimientoInventarioExcelAPI
from inventarios.views import SeccionAlmacenAPI

from trabajos.views import OrdenTrabajoAPI
from trabajos.views import OrdenTrabajoLastAPI
from trabajos.views import OrdenAnexoTextoAPI
from trabajos.views import OrdenAnexoImagenAPI
from trabajos.views import OrdenAnexoArchivoAPI
from trabajos.views import OrdenTrabajoExcelAPI
from trabajos.views import ActividadAPI
from trabajos.views import ManoObraAPI
from trabajos.views import MaterialAPI
from trabajos.views import ServicioExternoAPI
from trabajos.views import ActividadDetalleAPI
from trabajos.views import SolicitudCompraEncabezadoAPI
from trabajos.views import SolicitudCompraEncabezadoExcelAPI
from trabajos.views import SolicitudCompraDetalleAPI
from trabajos.views import SolicitudCompraDetalleExcelAPI

from seguridad.views import UserAPI
from seguridad.views import ProfileAPI
from seguridad.views import ProfileExcelAPI

from programaciones.views import ProgramaAPI

from comunicacion.views import MensajeAPI

from administracion.views import EmpresaAPI

# Librerias necesarias para publicar Medias en DEBUG
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter()

# ----------------- EQUIPOS ----------------- #

router.register(
    r'equipos',
    EquipoAPI,
    'equipo'
)
router.register(
    r'equipoorden',
    EquipoOrdenAPI,
    'equipoorden'
)
router.register(
    r'equipoexcel',
    EquipoExcelAPI,
    'equipoexcel'
)

# ----------------- USUARIOS ----------------- #

router.register(
    r'users',
    UserAPI,
    'user'
)

# ----------------- PROFILE ----------------- #

router.register(
    r'profiles',
    ProfileAPI,
    'profile'
)
router.register(
    r'profilesexcel',
    ProfileExcelAPI,
    'profileexcel'
)


# ----------------- EQUIPOS - ANEXOS ----------------- #

router.register(
    r'anexostexto',
    AnexoTextoAPI,
    'anexotexto'
)
router.register(
    r'anexosarchivo',
    AnexoArchivoAPI,
    'anexoarchivo'
),
router.register(
    r'anexosimagen',
    AnexoImagenAPI,
    'anexoimagen'
)

# ----------------- UBICACIONES ----------------- #

router.register(
    r'ubicaciones',
    UbicacionAPI,
    'ubicacion'
)
router.register(
    r'ubicaciones2',
    UbicacionAPI2,
    'ubicacion2'
)


# ----------------- ODOMETROS ----------------- #

router.register(
    r'odometros',
    OdometroAPI,
    'odometro'
)
router.register(
    r'odometroexcel',
    OdometroExcelAPI,
    'odometroexcel'
)

# ----------------- UDMS - ODOMETRO ----------------- #

router.register(
    r'udmodometro',
    UdmOdometroAPI,
    'udmodometro'
)
router.register(
    r'udmodometro2',
    UdmOdometroAPI2,
    'udmodometro2'
)
# -----------------TIPO ODOMETRO ----------------- #

router.register(
    r'tipoodometro',
    TipoOdometroAPI,
    'tipoodometro'
)

# ----------------- MEDICIONES ----------------- #

router.register(
    r'mediciones',
    MedicionAPI,
    'medicion'
)
router.register(
    r'medicionexcel',
    MedicionExcelAPI,
    'medicionexcel'
)

# ----------------- ALMACENES ----------------- #

router.register(
    r'almacenes',
    AlmacenAPI,
    'almacen'
)
router.register(
    r'almacenes2',
    AlmacenAPI2,
    'almacen'
)
router.register(
    r'seccionalmacen',
    SeccionAlmacenAPI,
    'seccionalmacen'
)

# ----------------- ARTICULO - UDM ----------------- #

router.register(
    r'udmarticulo',
    UdmArticuloAPI,
    'udmarticulo'
)
router.register(
    r'udmarticulo2',
    UdmArticuloAPI2,
    'udmarticulo2'
)

# ----------------- ARTICULOS ----------------- #

router.register(
    r'articulos',
    ArticuloAPI,
    'articulo'
)

router.register(
    r'articulos2',
    ArticuloAPI2,
    'articulo2'
)

router.register(
    r'articulosforordenes',
    ArticuloForOrdenesAPI,
    'articulosforordenes'
)

router.register(
    r'articulosforpersonal',
    ArticuloForPersonalAPI,
    'articulosforpersonal'
)

# ----------------- STOCK ----------------- #
router.register(
    r'stock',
    StockAPI,
    'stock'
)
router.register(
    r'stockexcel',
    StockExcelAPI,
    'stockexcel'
)


# ----------------- ARTICULOS - ANEXOS ----------------- #

router.register(
    r'articulosanexotexto',
    ArticuloAnexoTextoAPI,
    'articuloanexotexto'
)
router.register(
    r'articulosanexoimagen',
    ArticuloAnexoImagenAPI,
    'articuloanexoimagen'
)
router.register(
    r'articulosanexoarchivo',
    ArticuloAnexoArchivoAPI,
    'articuloanexoarchivo'
)


# ----------------- ORDENES DE TRABAJO ----------------- #

router.register(
    r'ordenestrabajo',
    OrdenTrabajoAPI,
    'ordentrabajo'
)
router.register(
    r'ordenestrabajoexcel',
    OrdenTrabajoExcelAPI,
    'ordentrabajoexcel'
)

router.register(
    r'ordenestrabajolast',
    OrdenTrabajoLastAPI,
    'ordentrabajolast'
)

# ----------------- ACTIVIDAD ----------------- #

router.register(
    r'actividades',
    ActividadAPI,
    'actividad'
)
router.register(
    r'actividaddetalles',
    ActividadDetalleAPI,
    'actividaddetalle'
)

# ----------------- MANO OBRA ----------------- #

router.register(
    r'manoobra',
    ManoObraAPI,
    'manoobra'
)


# ----------------- MATERIAL ----------------- #

router.register(
    r'materiales',
    MaterialAPI,
    'material'
)


# ----------------- SERVICIO EXTERNO ----------------- #

router.register(
    r'servicioexterno',
    ServicioExternoAPI,
    'servicioexterno'
)


# ----------------- ORDENES DE TRABAJO - ANEXOS ----------------- #

router.register(
    r'ordenesanexotexto',
    OrdenAnexoTextoAPI,
    'ordenanexotexto'
)
router.register(
    r'ordenesanexoimagen',
    OrdenAnexoImagenAPI,
    'ordenanexoimagen'
)
router.register(
    r'ordenesanexoarchivo',
    OrdenAnexoArchivoAPI,
    'ordenanexoarchivo'
)

# ----------------- ENTRADAS  ----------------- #

router.register(
    r'movimientos',
    MovimientoAPI,
    'movimientocabecera'
)
router.register(
    r'movimientoexcel',
    MovimientoExcelAPI,
    'movimientoexcel'
)
router.register(
    r'movimientosdetalle',
    MovimientoDetalleAPI,
    'movimientodetalle'
)
router.register(
    r'movimientosdetalleexcel',
    MovimientoDetalleExcelAPI,
    'movimientodetalleexcel'
)

router.register(
    r'inventario',
    MovimientoInventarioAPI,
    'movimientoinventario'
)
router.register(
    r'inventarioexcel',
    MovimientoInventarioExcelAPI,
    'movimientoinventarioexcel'
)

# ----------------- SOLICITUD DE COMPRA ----------------- #
router.register(
    r'solicitudescompra',
    SolicitudCompraEncabezadoAPI,
    'solicitudcompraencabezado'
)
router.register(
    r'solicitudescompraexcel',
    SolicitudCompraEncabezadoExcelAPI,
    'solicitudcompraencabezadoexcel'
)
router.register(
    r'solicitudescompradetalles',
    SolicitudCompraDetalleAPI,
    'solicitudcompradetalle'
)
router.register(
    r'solicitudescompradetalleexcel',
    SolicitudCompraDetalleExcelAPI,
    'solicitudcompradetalleexcel'
)

# ----------------- PROGRAMACIONES ----------------- #
router.register(
    r'programas',
    ProgramaAPI,
    'programa'
)

# ----------------- COMUNICACION ----------------- #
router.register(
    r'mensajes',
    MensajeAPI,
    'mensaje'
)

# ----------------- EMPRESA ----------------- #
router.register(
    r'empresas',
    EmpresaAPI,
    'empresa'
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'', include('administracion.urls', namespace="administracion")),
    url(r'', include('seguridad.urls', namespace="seguridad")),
    url(r'', include('activos.urls', namespace="activos")),
    url(r'', include('inventarios.urls', namespace="inventarios")),
    url(r'', include('trabajos.urls', namespace="trabajos")),
    url(r'', include('dashboards.urls', namespace="dashboards")),
    url(r'', include('home.urls', namespace="home")),
    url(r'', include('programaciones.urls', namespace="programaciones")),
    url(r'', include('comunicacion.urls', namespace="comunicacion")),
    url(r'', include('ti.urls', namespace="ti")),

    url(r'^report_builder/', include('report_builder.urls'))
]


if settings.DEBUG:

    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
