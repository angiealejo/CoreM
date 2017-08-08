# -*- coding: utf-8 -*-

# Django Atajos:
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.core.exceptions import PermissionDenied

# Django Urls:
from django.core.urlresolvers import reverse

# Django Generic Views
from django.views.generic.base import View
from django.views.generic import ListView

# Django Seguridad
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Modelos:
from .models import Contrato
from .models import Empresa

# Formularios:
from .forms import ContratoForm
from .forms import EmpresaForm

# API REST
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


# Serializers

from .serializers import EmpresaSerializer
# ----------------- CONTRATO ----------------- #


@method_decorator(login_required, name='dispatch')
class ContratoListView(ListView):

    template_name = 'contrato/lista.html'
    model = Contrato
    context_object_name = 'registros'
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class ContratoCreateView(View):

    def __init__(self):
        self.template_name = 'contrato/formulario.html'

    def get(self, request):
        formulario = ContratoForm()
        contexto = {
            'form': formulario,
            'operation': "Nuevo"
        }

        return render(request, self.template_name, contexto)

    def post(self, request):

        formulario = ContratoForm(request.POST, request.FILES)

        if formulario.is_valid():

            datos_formulario = formulario.cleaned_data
            contrato = Contrato()

            contrato.clave = datos_formulario.get('clave')
            contrato.nombre = datos_formulario.get('nombre')
            contrato.descripcion = datos_formulario.get('descripcion')
            contrato.cliente = datos_formulario.get('cliente')
            contrato.numero = datos_formulario.get('numero')
            contrato.region = datos_formulario.get('region')
            contrato.estado = datos_formulario.get('estado')

            contrato.created_by = request.user

            contrato.save()

            return redirect(
                reverse('administracion:contratos_lista')
            )

        contexto = {
            'form': formulario,
            'operation': "Nuevo"
        }
        return render(request, self.template_name, contexto)


@method_decorator(login_required, name='dispatch')
class ContratoUpdateView(View):

    def __init__(self):
        self.template_name = 'contrato/formulario.html'

    def get(self, request, pk):

        contrato = get_object_or_404(Contrato, pk=pk)

        formulario = ContratoForm(
            instance=contrato
        )

        contexto = {
            'form': formulario,
            'operation': "Editar",
        }

        return render(request, self.template_name, contexto)

    def post(self, request, pk):

        contrato = get_object_or_404(Contrato, pk=pk)

        formulario = ContratoForm(
            request.POST, request.FILES, instance=contrato)

        if formulario.is_valid():

            contrato = formulario.save(commit=False)
            contrato.updated_by = request.user
            contrato.save()

            return redirect(
                reverse('administracion:contratos_lista')
            )

        contexto = {
            'form': formulario,
            'operation': "Editar",
        }
        return render(request, self.template_name, contexto)


# ----------------- ADMINISTRACION ----------------- #

@method_decorator(login_required, name='dispatch')
class EmpresaListView(ListView):

    template_name = 'empresa/lista.html'
    model = Empresa
    context_object_name = 'registros'
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class EmpresaCreateView(View):

    def __init__(self):
        self.template_name = "empresa/formulario.html"

    def get(self, request):
        if not request.user.is_staff:
            raise PermissionDenied

        formulario = EmpresaForm()
        contexto = {
            'form': formulario,
            'operation': 'Nuevo'
        }
        return render(request, self.template_name, contexto)

    def post(self, request):
        formulario = EmpresaForm(request.POST, request.FILES)

        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            empresa = Empresa()
            empresa.clave = datos_formulario.get('clave')
            empresa.descripcion = datos_formulario.get('descripcion')
            empresa.logo = datos_formulario.get('logo')
            empresa.save()

            return redirect(reverse('administracion:empresas_lista'))

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
        }

        return render(request, self.template_name, contexto)


@method_decorator(login_required, name='dispatch')
class EmpresaUpdateView(View):

    def __init__(self):
        self.template_name = "empresa/formulario.html"

    def obtener_UrlImagen(self, _imagen):
        imagen = ''

        if _imagen:
            imagen = _imagen.url

        return imagen

    def get(self, request, pk):
        if not request.user.is_staff:
            raise PermissionDenied

        empresa = get_object_or_404(Empresa, pk=pk)
        formulario = EmpresaForm(instance=empresa)

        contexto = {
            'form': formulario,
            'operation': 'Editar',
            'logo': self.obtener_UrlImagen(empresa.logo)
        }

        return render(request, self.template_name, contexto)

    def post(self, request, pk):

        empresa = get_object_or_404(Empresa, pk=pk)
        formulario = EmpresaForm(request.POST, request.FILES, instance=empresa)

        if formulario.is_valid():
            empresa = formulario.save(commit=False)
            empresa.save()

            return redirect(reverse('administracion:empresas_lista'))

        contexto = {
            'form': formulario,
            'operation': 'Editar',
            'logo': self.obtener_UrlImagen(empresa.logo)
        }

        return render(request, self.template_name, contexto)


class EmpresaAPI(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)
