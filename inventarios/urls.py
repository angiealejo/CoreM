# -*- coding: utf-8 -*-

# Librerias Django:
from django.conf.urls import url

# Autenticacion
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

# Vistas:
from .views import AlmacenListView
from .views import AlmacenCreateView
from .views import AlmacenUpdateView

from .views import StockListView

from .views import UdmArticuloListView
from .views import UdmArticuloCreateView
from .views import UdmArticuloUpdateView

from .views import ArticuloListView
from .views import ArticuloCreateView
from .views import ArticuloUpdateView

from .views import ArticuloAnexoTextoView
from .views import ArticuloAnexoImagenView
from .views import ArticuloAnexoArchivoView

from .views import EntradaSaldoListView
from .views import EntradaSaldoCreateView
from .views import EntradaSaldoUpdateView
from .views import EntradaCompraListView
from .views import EntradaCompraCreateView
from .views import EntradaCompraUpdateView
from .views import EntradaAjusteListView
from .views import EntradaAjusteCreateView
from .views import EntradaAjusteUpdateView
# from .views import EntradaTransitoListView
from .views import EntradaTraspasoListView
# from .views import EntradaTraspasoDetailView
from .views import EntradaTransitoReceiveView
from .views import SalidaPersonalListView
from .views import SalidaPersonalCreateView
from .views import SalidaPersonalUpdateView
from .views import SalidaOrdenTrabajoListView
from .views import SalidaOrdenTrabajoCreateView
from .views import SalidaOrdenTrabajoUpdateView
from .views import SalidaAjusteListView
from .views import SalidaAjusteCreateView
from .views import SalidaAjusteUpdateView
from .views import SalidaTraspasoListView
from .views import SalidaTraspasoCreateView
from .views import SalidaTraspasoUpdateView
from .views import MovimientoListView
from .views import MovimientoDetailView
from .views import ReporteAPI
from .views import EntradaTransitoCountAPI

app_name = "inventarios"

urlpatterns = [
    url(
        r'^reporte/$', login_required
        (ReporteAPI.as_view()),
        name='almacenes_lista'
    ),
    # ----------------- ALMACEN ----------------- #

    url(
        r'^almacenes/$',
        (AlmacenListView.as_view()),
        name='almacenes_lista'
    ),
    url(
        r'^almacenes/nuevo/$',
        (AlmacenCreateView.as_view()),
        name='almacenes_nuevo'
    ),
    url(
        r'^almacenes/editar/(?P<pk>.*)/$',
        (AlmacenUpdateView.as_view()),
        name='almacenes_editar'
    ),


    # ----------------- UDM ARTICULO ----------------- #

    url(
        r'udmarticulo/$',
        (UdmArticuloListView.as_view()),
        name='udms_articulo_lista'
    ),
    url(
        r'udmarticulo/nuevo/$',
        (UdmArticuloCreateView.as_view()),
        name='udms_articulo_nuevo'
    ),
    url(
        r'udmarticulo/editar/(?P<pk>\d+)/$',
        (UdmArticuloUpdateView.as_view()),
        name='udms_articulo_editar'
    ),



    # ----------------- ARTICULOS ----------------- #

    url(
        r'^articulos/$',
        login_required(ArticuloListView.as_view()),
        name='articulos_lista'
    ),
    url(
        r'^articulos/nuevo/$',
        (ArticuloCreateView.as_view()),
        name='articulos_nuevo'
    ),
    url(
        r'^articulos/editar/(?P<pk>.*)/$',
        (ArticuloUpdateView.as_view()),
        name='articulos_editar'
    ),


    # ----------------- ARTICULOS - ANEXOS ----------------- #

    url(
        r'articulos/anexos/(?P<pk>\d+)/texto/$',
        ArticuloAnexoTextoView.as_view(),
        name='anexar_texto'
    ),
    url(
        r'^articulos/anexos/(?P<pk>\d+)/imagen/$',
        ArticuloAnexoImagenView.as_view(),
        name='anexar_imagen'
    ),
    url(
        r'^articulos/anexos/(?P<pk>\d+)/archivo/$',
        ArticuloAnexoArchivoView.as_view(),
        name='anexar_archivo'
    ),


    # ----------------- STOCK ----------------- #

    url(
        r'^stock/(?P<almacen>\d+)/(?P<articulo>\d+)/$',
        login_required(StockListView.as_view()),
        name='stock'
    ),


    # ----------------- ENTRADAS ----------------- #

    url(
        r'entradas/saldo_inicial/$',
        login_required(EntradaSaldoListView.as_view()),
        name='entradas_saldoinicial_lista'
    ),
    url(
        r'entradas/saldo_inicial/nuevo/$',
        login_required(EntradaSaldoCreateView.as_view()),
        name='entradas_saldoinicial_nuevo'
    ),
    url(
        r'entradas/saldo_inicial/editar/(?P<pk>\d+)/$',
        login_required(EntradaSaldoUpdateView.as_view()),
        name='entradas_saldoinicial_editar'
    ),
    url(
        r'entradas/compras/$',
        login_required(EntradaCompraListView.as_view()),
        name='entradas_compras_lista'
    ),
    url(
        r'entradas/compras/nuevo/$',
        login_required(EntradaCompraCreateView.as_view()),
        name='entradas_compras_nuevo'
    ),
    url(
        r'entradas/compras/editar/(?P<pk>\d+)/$',
        login_required(EntradaCompraUpdateView.as_view()),
        name='entradas_compras_editar'
    ),
    url(
        r'entradas/ajustes/$',
        login_required(EntradaAjusteListView.as_view()),
        name='entradas_ajustes_lista'
    ),
    url(
        r'entradas/ajustes/nuevo/$',
        login_required(EntradaAjusteCreateView.as_view()),
        name='entradas_ajustes_nuevo'
    ),
    url(
        r'entradas/ajustes/editar/(?P<pk>\d+)/$',
        login_required(EntradaAjusteUpdateView.as_view()),
        name='entradas_ajuste_editar'
    ),
    url(
        r'entradas/traspaso/$',
        login_required(EntradaTraspasoListView.as_view()),
        name='entradas_traspaso_lista'
    ),
    url(
        r'entradas/traspaso/(?P<estado>\w+)/$',
        login_required(EntradaTraspasoListView.as_view()),
        name='entradas_traspaso_lista'
    ),
    url(
        r'entradas/traspaso/ver/(?P<pk>\d+)/$',
        login_required(EntradaTransitoReceiveView.as_view()),
        name='entradas_traspaso_recibir1'
    ),
    # ----------------- SALIDAS ----------------- #
    url(
        r'salidas/personal/$',
        login_required(SalidaPersonalListView.as_view()),
        name='salidas_personal_lista'
    ),
    url(
        r'salidas/personal/nuevo/$',
        login_required(SalidaPersonalCreateView.as_view()),
        name='salidas_personal_nuevo'
    ),
    url(
        r'salidas/personal/editar/(?P<pk>\d+)/$',
        login_required(SalidaPersonalUpdateView.as_view()),
        name='salidas_personal_editar'
    ),
    url(
        r'salidas/orden_trabajo/$',
        login_required(SalidaOrdenTrabajoListView.as_view()),
        name='salidas_ordentrabajo_lista'
    ),
    url(
        r'salidas/orden_trabajo/nuevo/$',
        login_required(SalidaOrdenTrabajoCreateView.as_view()),
        name='salidas_ordentrabajo_nuevo'
    ),
    url(
        r'salidas/orden_trabajo/editar/(?P<pk>\d+)/$',
        login_required(SalidaOrdenTrabajoUpdateView.as_view()),
        name='salidas_ordentrabajo_editar'
    ),
    url(
        r'salidas/ajustes/$',
        login_required(SalidaAjusteListView.as_view()),
        name='salidas_ajustes_lista'
    ),
    url(
        r'salidas/ajustes/nuevo/$',
        login_required(SalidaAjusteCreateView.as_view()),
        name='salidas_ajustes_nuevo'
    ),
    url(
        r'salidas/ajustes/editar/(?P<pk>\d+)/$',
        login_required(SalidaAjusteUpdateView.as_view()),
        name='salidas_ajustes_editar'
    ),
    url(
        r'salidas/traspaso/$',
        login_required(SalidaTraspasoListView.as_view()),
        name='salidas_traspaso_lista'
    ),
    url(
        r'salidas/traspaso/nuevo/$',
        login_required(SalidaTraspasoCreateView.as_view()),
        name='salidas_traspaso_nuevo'
    ),
    url(
        r'salidas/traspaso/editar/(?P<pk>\d+)/$',
        login_required(SalidaTraspasoUpdateView.as_view()),
        name='salidas_traspaso_editar'
    ),
    # -------- MOVIMIENTOS AL ALMACEN ---------------- #
    url(
        r'movimientos/$',
        login_required(MovimientoListView.as_view()),
        name='movimientos_almacen_lista'
    ),
    url(
        r'movimientos/detalle/(?P<pk>\d+)/$',
        login_required(MovimientoDetailView.as_view()),
        name='movimientos_almacen_detalle'
    ),

    # --------------------- API ---------------------- #
    url(
        r'^entradastransito/$',
        login_required(EntradaTransitoCountAPI.as_view()),
        name='entradas_transito_count'
    ),
]
