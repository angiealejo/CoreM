# -*- coding: utf-8 -*-

# Django Atajos:
from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Django Seguridad:
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Django Generic Views
from django.views.generic.base import View

# Django Busqueda
from django.db.models import Q

# API Rest & Json:
from rest_framework import viewsets

# Models:
from .models import Mensaje

# Serializadores:
from .serializers import MensajeSerializer

# Django paginacion:
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


class MensajeAPI(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all().order_by("-created_date")[:10]
    serializer_class = MensajeSerializer


@method_decorator(login_required, name='dispatch')
class MensajeHistorialView(View):

    def __init__(self):
        self.template_name = 'mensaje/mensaje_historial.html'

    def get(self, request):

        query = request.GET.get('q')
        if query:
            mensaje_lista = Mensaje.objects.filter(
                Q(usuario__username__icontains=query) |
                Q(usuario__first_name__icontains=query) |
                Q(usuario__last_name__icontains=query) |
                Q(texto__icontains=query)
            ).order_by("-created_date")
        else:
            mensaje_lista = Mensaje.objects.all().order_by("-created_date")

        paginator = Paginator(mensaje_lista, 10)
        page = request.GET.get('page')

        try:
            mensajes = paginator.page(page)
        except PageNotAnInteger:
            mensajes = paginator.page(1)
        except EmptyPage:
            mensajes = paginator.page(paginator.num_pages)

        contexto = {
            'mensajes': mensajes
        }

        return render(request, self.template_name, contexto)


@method_decorator(login_required, name='dispatch')
class MensajeView(View):

    def __init__(self):
        self.template_name = 'mensaje/mensaje_view.html'

    def get(self, request, pk):
        mensaje = get_object_or_404(Mensaje, pk=pk)

        contexto = {
            'mensaje': mensaje
        }

        return render(request, self.template_name, contexto)
