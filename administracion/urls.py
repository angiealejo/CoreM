# -*- coding: utf-8 -*-

# Librerias Django:
from django.conf.urls import url

# Autenticacion
from django.contrib.auth.decorators import permission_required


# Vistas:
from .views import ContratoListView
from .views import ContratoCreateView
from .views import ContratoUpdateView

from .views import EmpresaListView
from .views import EmpresaCreateView
from .views import EmpresaUpdateView

app_name = "administracion"

urlpatterns = [

    # ----------------- CONTRATOS ----------------- #
    url(
        r'^contratos/$',
        permission_required('is_staff', raise_exception=True)
        (ContratoListView.as_view()),
        name='contratos_lista'
    ),
    url(
        r'^contratos/nuevo/$',
        permission_required('is_staff', raise_exception=True)
        (ContratoCreateView.as_view()),
        name='contratos_nuevo'
    ),
    url(
        r'^contratos/editar/(?P<pk>.*)/$',
        permission_required('is_staff', raise_exception=True)
        (ContratoUpdateView.as_view()),
        name='contratos_editar'
    ),


    # ----------------- EMPRESAS ----------------- #
    url(
        r'^empresas/$',
        EmpresaListView.as_view(),
        name='empresas_lista'
    ),
    url(
        r'^empresas/nuevo/$',
        EmpresaCreateView.as_view(),
        name='empresas_nuevo'
    ),
    url(
        r'^empresas/editar/(?P<pk>\d+)/$',
        EmpresaUpdateView.as_view(),
        name='empresas_editar'
    ),
]
