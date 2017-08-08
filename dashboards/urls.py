# -*- coding: utf-8 -*-

# Librerias Django:

# Urls
from django.conf.urls import url

# Vistas
from .views import Inicio

app_name = "dashboards"

urlpatterns = [
    url(
        r'^inicio/$',
        Inicio.as_view(),
        name='inicio'
    ),
]
