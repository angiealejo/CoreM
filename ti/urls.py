# -*- coding: utf-8 -*-

# Librerias Django:

# Urls
from django.conf.urls import url
from .views import FixAlmacenView


app_name = "ti"

urlpatterns = [

    url(
        r'^fix/almacen/$',
        FixAlmacenView.as_view(),
        name='fix_almacen'
    ),
]
