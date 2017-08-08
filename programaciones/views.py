# -*- coding: utf-8 -*-

# LIBRERIAS Django

# Django Atajos:
from django.shortcuts import render

# Django Generic Views:
from django.views.generic.base import View

# Modelos:
from .models import Programa

# Serializadores:
from .serializers import ProgramaSerializer

# API Rest:
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

# API Rest Filtros:
from .filters import ProgramaFilter


class ProgamaLista(View):

    def __init__(self):
        self.template_name = 'programa/lista.html'

    def get(self, request):

        # formulario = ArticuloFilterForm()

        # contexto = {
        #     'form': formulario
        # }

        return render(request, self.template_name, {})

    def post(self, request):
        return render(request, self.template_name, {})


class ProgramaAPI(viewsets.ModelViewSet):
    queryset = Programa.objects.all()
    serializer_class = ProgramaSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProgramaFilter
