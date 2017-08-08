# -*- coding: utf-8 -*-

# Librerias Django:

# Urls
from django.conf.urls import url


# Vistas
from .views import MensajeHistorialView
from .views import MensajeView

app_name = "comunicacion"

urlpatterns = [

    url(
        r'^mensajes/historial/$',
        MensajeHistorialView.as_view(),
        name='mensajes_historial'
    ),
    url(
        r'^mensajes/revisar/(?P<pk>.*)/$',
        MensajeView.as_view(),
        name='mensajes_revisar'
    ),
]
