# -*- coding: utf-8 -*-

# Librerias Django:
from django.conf.urls import url

# Autenticacion:
from django.contrib.auth.decorators import login_required

# Vistas:
from .views import ProgamaLista

app_name = "programaciones"

urlpatterns = [
    url(
        r'^programa/$',
        login_required(ProgamaLista.as_view()),
        name='programa_lista'
    ),
]
