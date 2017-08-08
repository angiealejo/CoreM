# -*- coding: utf-8 -*-

# Librerias django:
from django.conf.urls import url

# Vistas:
from .views import Index
from .views import Error

urlpatterns = [
    url(r'^index/$', Index.as_view(), name='home.index'),
    url(r'^error/$', Error.as_view(), name='error.index'),
]
