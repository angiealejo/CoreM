# -*- coding: utf-8 -*-

# Librerias Django:

# Urls
from django.conf.urls import url

# Aplicacion
from django.conf import settings

# Autenticacion
from django.contrib.auth import views as auth_views

# Vistas
from .views import Login
from .views import UsuarioListView
from .views import UsuarioCreateView
from .views import UsuarioEditView
from .views import UsuarioPerfilView

app_name = "seguridad"

urlpatterns = [

    # ----------------- SEGURIDAD ----------------- #
    url(
        r'^$',
        Login.as_view(),
        name='login'
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'next_page': settings.LOGIN_URL},
        name='logout'
    ),

    # ----------------- USUARIO ----------------- #
    url(
        r'^usuarios/$',
        UsuarioListView.as_view(),
        name='usuarios_lista'
    ),
    url(
        r'^usuarios/nuevo/$',
        UsuarioCreateView.as_view(),
        name='usuarios_nuevo'
    ),
    url(
        r'^usuarios/editar/(?P<pk>.*)/$',
        UsuarioEditView.as_view(),
        name='usuarios_editar'
    ),
    url(
        r'^usuarios/perfil/(?P<pk>.*)/$',
        UsuarioPerfilView.as_view(),
        name='usuarios_perfil'
    ),
]
