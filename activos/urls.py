# -*- coding: utf-8 -*-

# Librerias Django:
from django.conf.urls import url

# Autenticacion
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

# Vistas:
from .views import EquipoListView
from .views import EquipoCreateView
from .views import EquipoUpdateView
from .views import EquipoTreeListView
from .views import EquipoHistory
from .views import EquipoTreeAPI
from .views import EquipoTreeAPI2

from .views import OdometroListView
from .views import OdometroCreateView
from .views import OdometroUpdateView

from .views import AnexoTextoView
from .views import AnexoImagenView
from .views import AnexoArchivoView

from .views import UbicacionCreateView
from .views import UbicacionListView
from .views import UbicacionUpdateView

from .views import UdmOdometroCreateView
from .views import UdmOdometroListView
from .views import UdmOdometroUpdateView

from .views import MedicionOdometroView
from .views import MedicionView
from .views import MedicionHistorialView
from .views import reporte_mensual
from .views import ReporteView
from .views import CapturaView
from .views import CapturaMedicionView

from .views import TipoOdometroListView
from .views import TipoOdometroCreateView
from .views import TipoOdometroUpdateView
from .views import MedicionHistory
from .views import reporte_seguimiento_operativo
# from .views import SistemaListView
# from .views import SistemaCreateView
# from .views import SistemaUpdateView

app_name = "activos"

urlpatterns = [
    # --------------- MEDICIONES ------------------ #
    url(
        r'^mediciones/$', permission_required('is_staff', raise_exception=True)
        (MedicionView.as_view()),
        name='equipos_mediciones'
    ),
    url(
        r'^mediciones/historial/equipo/(?P<equipo>\d+)/tipo_odometro/(?P<tipo_odometro>\d+)/$',
        permission_required('is_staff', raise_exception=True)
        (MedicionHistorialView.as_view()),
        name='mediciones_historial'
    ),
    url(
        r'^mediciones/captura/$', login_required
        (CapturaView.as_view()),
        name='mediciones_captura'
    ),
    url(
        r'^mediciones/captura/(?P<equipo>\d+)/$', login_required
        (CapturaView.as_view()),
        name='mediciones_captura'
    ),
    url(
        r'^mediciones/capturar/$', login_required
        (CapturaMedicionView.as_view()),
        name='mediciones_capturar'
    ),
    url(
        r'^mediciones/capturar/(?P<equipo>\d+)/$', login_required
        (CapturaMedicionView.as_view()),
        name='mediciones_capturar'
    ),
    # --------------- REPORTE SEGUIMIENTO OPERATIVO ------------------ #
    url(
        r'^reporte_seguimiento_operativo/$', login_required
        (reporte_seguimiento_operativo),
        name='reporte_seguimiento_operativo'
    ),
    url(
        r'^mediciones/historia/$', login_required
        (MedicionHistory.as_view()),
        name='mediciones_historia'
    ),
    url(
        r'^mediciones/log/(?P<equipo>\d+)/(?P<tipo_odometro>\d+)/$', login_required
        (MedicionHistory.as_view()),
        name='mediciones_log'
    ),

    # ----------------- EQUIPO ----------------- #
    url(
        r'^equipos/$', login_required
        (EquipoListView.as_view()),
        name='equipos_lista'
    ),
    url(
        r'^equipos/nuevo/$', permission_required('is_staff', raise_exception=True)
        (EquipoCreateView.as_view()),
        name='equipos_nuevo'
    ),
    url(
        r'^equipos/editar/(?P<pk>.*)/$',
        (EquipoUpdateView.as_view()),
        name='equipos_editar'
    ),
    url(
        r'equipos/arbol/(?P<pk>\d+)/$', login_required
        (EquipoTreeListView.as_view()),
        name='equipos_arbol'
    ),
    url(
        r'^equipos/arbol/json/(?P<pk>\d+)/$',
        EquipoTreeAPI.as_view(),
        name='equipos_api_tree'
    ),
    url(
        r'^equipos/arbol2/json/(?P<q>\w+)/$',
        EquipoTreeAPI2.as_view(),
        name='equipos_api2_tree'
    ),
    url(
        r'^equipos/historia/(?P<pk>.*)/$', permission_required('is_staff', raise_exception=True)
        (EquipoHistory.as_view()),
        name='equipos_historia'
    ),
    # ----------------- ANEXOS ------------------ #

    url(
        r'equipos/anexos/(?P<pk>\d+)/texto/$',
        AnexoTextoView.as_view(),
        name='anexar_texto'
    ),
    url(
        r'^equipos/anexos/(?P<pk>\d+)/imagen/$',
        AnexoImagenView.as_view(),
        name='anexar_imagen'
    ),
    url(
        r'^equipos/anexos/(?P<pk>\d+)/archivo/$',
        AnexoArchivoView.as_view(),
        name='anexar_archivo'
    ),

    # ----------------- UBICACION ----------------- #

    url(
        r'ubicaciones/$',
        (UbicacionListView.as_view()),
        name='ubicaciones_lista'
    ),
    url(
        r'^ubicaciones/nuevo/$', permission_required('is_staff', raise_exception=True)
        (UbicacionCreateView.as_view()),
        name='ubicaciones_nuevo'
    ),
    url(
        r'^ubicaciones/editar/(?P<pk>\d+)/$', permission_required('is_staff', raise_exception=True)
        (UbicacionUpdateView.as_view()),
        name='ubicaciones_editar'
    ),


    # ----------------- UDM ODOMETRO ----------------- #

    url(
        r'udmodometro/$', permission_required('is_staff', raise_exception=True)
        (UdmOdometroListView.as_view()),
        name='udms_odometro_lista'
    ),
    url(
        r'udmodometro/nuevo/$', permission_required('is_staff', raise_exception=True)
        (UdmOdometroCreateView.as_view()),
        name='udms_odometro_nuevo'
    ),
    url(
        r'udmodometro/editar/(?P<pk>\d+)/$', permission_required('is_staff', raise_exception=True)
        (UdmOdometroUpdateView.as_view()),
        name='udms_odometro_editar'
    ),

    # ----------------- ODOMETRO ----------------- #
    url(
        r'^odometros/$', login_required
        (OdometroListView.as_view()),
        name='odometros_lista'
    ),
    url(
        r'^odometros/nuevo/$', permission_required('is_staff', raise_exception=True)
        (OdometroCreateView.as_view()),
        name='odometros_nuevo'
    ),
    url(
        r'^odometros/editar/(?P<pk>.*)/$', permission_required('is_staff', raise_exception=True)
        (OdometroUpdateView.as_view()),
        name='odometros_lista'
    ),

    #  ----------------- SISTEMA ----------------- #

    # url(
    #     r'^sistemas/$',
    #     SistemaListView.as_view(),
    #     name='sistemas_lista'
    # ),
    # url(
    #     r'^sistemas/nuevo/$',
    #     SistemaCreateView.as_view(),
    #     name='sistemas_nuevo'
    # ),
    # url(
    #     r'^sistemas/editar/(?P<pk>.*)/$',
    #     SistemaUpdateView.as_view(),
    #     name='sistemas_editar'
    # ),


    # ----------------- MEDICION ----------------- #

    url(
        r'^odometros/(?P<pk>.*)/mediciones/$', login_required
        (MedicionOdometroView.as_view()),
        name='odometros_mediciones'
    ),
    # ----------------- TIPO ODOMETRO ----------------- #
    url(
        r'^tipoodometro/$', login_required
        (TipoOdometroListView.as_view()),
        name='tipo_odometro_lista'
    ),
    url(
        r'^tipoodometro/nuevo/$', login_required
        (TipoOdometroCreateView.as_view()),
        name='tipo_odometro_nuevo'
    ),
    url(
        r'^tipoodometro/editar/(?P<pk>.*)/$', login_required
        (TipoOdometroUpdateView.as_view()),
        name='tipo_odometro_editar'
    ),

    # ----------------- REPORTES ----------------- #

    url(
        r'^reportes/', login_required
        (ReporteView.as_view()),
        name='reportes'
    ),
    url(
        r'^reporte_variables_operativas/', login_required
        (reporte_mensual),
        name='reporte_variables_operativas'
    )
]
