# -*- coding: utf-8 -*-

# LIBRERIAS Django

# Django DB
# from django.db import transaction

# Django Atajos:
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

# Django Urls:
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
# from django.http import HttpResponse

# Django Generic Views
from django.views.generic.base import View
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import TemplateView

# Django Messages
from django.contrib import messages
# Modelos:
# from .models import Udm
from .models import Articulo
from .models import UdmArticulo
from .models import Almacen
from .models import Stock
from .models import MovimientoCabecera
from .models import MovimientoDetalle
from .models import SeccionAlmacen
from home.models import AnexoImagen
from home.models import AnexoArchivo
from home.models import AnexoTexto

# Formularios:
from .forms import AlmacenForm
from .forms import ArticuloFilterForm
from .forms import ArticuloForm
from .forms import StockFilterForm
from .forms import UdmArticuloForm
from .forms import InventarioFiltersForm
from .forms import InventarioForm
from .forms import EntradaSaldoFiltersForm
from .forms import EntradaSaldoForm
from .forms import EntradaCompraFiltersForm
from .forms import EntradaCompraForm
from .forms import EntradaAjusteFiltersForm
from .forms import EntradaAjusteForm
from .forms import EntradaTraspasoFiltersForm
from .forms import SalidaPersonalFiltersForm
from .forms import SalidaPersonalForm
from .forms import SalidaOrdenTrabajoFiltersForm
from .forms import SalidaOrdenTrabajoForm
from .forms import SalidaAjusteFiltersForm
from .forms import SalidaAjusteForm
from .forms import SalidaTraspasoFiltersForm
from .forms import SalidaTraspasoForm
from home.forms import AnexoTextoForm
from home.forms import AnexoImagenForm
from home.forms import AnexoArchivoForm

# API Rest:
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# API Rest - Serializadores:
from .serializers import AlmacenSerializer
from .serializers import UdmArticuloSerializer
from .serializers import ArticuloSerializer
from .serializers import StockSerializer
from .serializers import MovimientoCabeceraSerializer
from .serializers import MovimientoDetalleSerializer
from .serializers import MovimientoInventarioSerializer
from .serializers import SeccionAlmacenSerializer
from .serializers import Reporte
from .serializers import ReporteSerializer
# from .serializers import SalidaCabeceraSerializer
from home.serializers import AnexoTextoSerializer
from home.serializers import AnexoImagenSerializer
from home.serializers import AnexoArchivoSerializer

# API Rest - Paginacion:
from .pagination import GenericPagination

# API Rest - Filtros:
from .filters import ArticuloFilter
from .filters import MovimientoCabeceraFilter
from .filters import StockFilter
from .filters import MovimientoInventarioFilter

# Clases de negocio:
from .business import EntradaAlmacenBusiness
from .business import SalidaAlmacenBusiness
from .business import TraspasoBusiness
from .business import SalidaOrdenTrabajoBusiness


class ReporteAPI(APIView):
    serializer_class = ReporteSerializer

    def get(self, request, format=None):

        articulos = Articulo.objects.all()

        for articulo in articulos:
            almacen = Almacen.objects.filter(articulos=articulo)
            stock = Stock.objects.filter(articulo=articulo)

            datos = Reporte(articulo, almacen, stock, "s", "sd")
            serializer = ReporteSerializer(data=datos)
            if serializer.is_valid():
                return Response(serializer.data)

        return Response(serializer.data)

# ----------------- ALMACEN ----------------- #


class AlmacenListView(TemplateView):
    template_name = 'almacen/lista.html'


class AlmacenCreateView(CreateView):

    def __init__(self):
        self.template_name = "almacen/formulario.html"

    def get(self, request):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            formulario = AlmacenForm()

            contexto = {
                'form': formulario,
                'operation': 'Nuevo'
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request):
        formulario = AlmacenForm(request.POST)
        # secciones = request.POST.getlist('seccion')
        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            almacen = Almacen()
            almacen.clave = datos_formulario.get('clave')
            almacen.descripcion = datos_formulario.get('descripcion')
            almacen.estado = datos_formulario.get('estado')
            almacen.save()
            # almacen.seccion = secciones
            # almacen.save()

            return redirect('inventarios:almacenes_lista')

        contexto = {
            'form': formulario,
        }

        return render(request, self.template_name, contexto)


class AlmacenUpdateView(UpdateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'almacen/formulario.html'
    success_url = reverse_lazy('inventarios:almacenes_lista')

    def get_context_data(self, **kwargs):
        context = super(AlmacenUpdateView, self).get_context_data(**kwargs)

        data = {
            'operation': "Editar"
        }

        context.update(data)

        return context


class AlmacenAPI(viewsets.ModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('clave', 'descripcion')


class AlmacenAPI2(viewsets.ModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)


class SeccionAlmacenAPI(viewsets.ModelViewSet):
    queryset = SeccionAlmacen.objects.all()
    serializer_class = SeccionAlmacenSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)

# ----------------- UDM ARTICULO ----------------- #


class UdmArticuloListView(TemplateView):
    template_name = 'udm_articulo/lista.html'


class UdmArticuloCreateView(CreateView):
    model = UdmArticulo
    form_class = UdmArticuloForm
    template_name = 'udm_articulo/formulario.html'
    success_url = reverse_lazy('inventarios:udms_articulo_lista')
    operation = "Nueva"

    def get_context_data(self, **kwargs):
        contexto = super(
            UdmArticuloCreateView,
            self
        ).get_context_data(**kwargs)
        contexto['operation'] = self.operation
        return contexto


class UdmArticuloUpdateView(UpdateView):
    model = UdmArticulo
    form_class = UdmArticuloForm
    template_name = 'udm_articulo/formulario.html'
    success_url = reverse_lazy('inventarios:udms_articulo_lista')
    operation = "Editar"

    def get_context_data(self, **kwargs):
        contexto = super(
            UdmArticuloUpdateView,
            self
        ).get_context_data(**kwargs)
        contexto['operation'] = self.operation
        return contexto


class UdmArticuloAPI(viewsets.ModelViewSet):
    queryset = UdmArticulo.objects.all()
    serializer_class = UdmArticuloSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('clave', 'descripcion',)


class UdmArticuloAPI2(viewsets.ModelViewSet):
    queryset = UdmArticulo.objects.all()
    serializer_class = UdmArticuloSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)


# ----------------- ARTICULOS ----------------- #


class ArticuloListView(View):
    def __init__(self):
        self.template_name = 'articulo/lista.html'

    def get(self, request):

        formulario = ArticuloFilterForm()

        contexto = {
            'form': formulario
        }

        return render(request, self.template_name, contexto)

    def post(self, request):
        return render(request, self.template_name, {})


class ArticuloCreateView(View):

    def __init__(self):
        self.template_name = 'articulo/formulario.html'

    def obtener_UrlImagen(self, _imagen):
        imagen = ''

        if _imagen:
            imagen = _imagen.url

        return imagen

    def get(self, request):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            formulario = ArticuloForm()
            contexto = {
                'form': formulario,
                'operation': "Nuevo"
            }
            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request):

        url_imagen = ""
        formulario = ArticuloForm(request.POST)

        if formulario.is_valid():

            datos_formulario = formulario.cleaned_data
            articulo = Articulo()
            articulo.clave = datos_formulario.get('clave')
            articulo.descripcion = datos_formulario.get('descripcion')
            articulo.tipo = datos_formulario.get('tipo')
            articulo.udm = datos_formulario.get('udm')
            articulo.observaciones = datos_formulario.get('observaciones')
            articulo.url = datos_formulario.get('url')
            articulo.marca = datos_formulario.get('marca')
            articulo.modelo = datos_formulario.get('modelo')
            articulo.numero_parte = datos_formulario.get('numero_parte')
            articulo.stock_minimo = datos_formulario.get('stock_minimo')
            articulo.stock_maximo = datos_formulario.get('stock_maximo')
            articulo.stock_seguridad = datos_formulario.get('stock_seguridad')
            articulo.estado = datos_formulario.get('estado')
            articulo.clave_jde = datos_formulario.get('clave_jde')
            articulo.imagen = datos_formulario.get('imagen')
            url_imagen = self.obtener_UrlImagen(articulo.imagen)

            articulo.save()

            return redirect(
                reverse('inventarios:articulos_lista')
            )
        contexto = {
            'form': formulario,
            'imagen': url_imagen,
            'operation': "Nuevo"
        }

        return render(request, self.template_name, contexto)


class ArticuloUpdateView(View):
    def __init__(self):
        self.template_name = 'articulo/formulario.html'

    def obtener_UrlImagen(self, _imagen):
        imagen = ''

        if _imagen:
            imagen = _imagen.url

        return imagen

    def get(self, request, pk):

        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            articulo = get_object_or_404(Articulo, pk=pk)

            formulario = ArticuloForm(
                instance=articulo
            )

            contexto = {
                'form': formulario,
                'operation': "Editar",
                'imagen': self.obtener_UrlImagen(articulo.imagen)
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):

        articulo = get_object_or_404(Articulo, pk=pk)
        formulario = ArticuloForm(
            request.POST,
            request.FILES,
            instance=articulo
        )

        if formulario.is_valid():

            articulo = formulario.save(commit=False)
            articulo.save()

            return redirect(
                reverse('inventarios:articulos_lista')
            )

        contexto = {
            'form': formulario,
            'operation': "Editar",
            'imagen': self.obtener_UrlImagen(articulo.imagen)
        }
        return render(request, self.template_name, contexto)


class ArticuloAPI(viewsets.ModelViewSet):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    pagination_class = GenericPagination

    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticuloFilter


class ArticuloAPI2(viewsets.ModelViewSet):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticuloFilter


class ArticuloForOrdenesAPI(viewsets.ModelViewSet):
    queryset = Articulo.objects.all().exclude(tipo__in=["HER", "EPP"])
    serializer_class = ArticuloSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticuloFilter


class ArticuloForPersonalAPI(viewsets.ModelViewSet):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticuloFilter

# ----------------- ARTICULO - ANEXOS ----------------- #


class ArticuloAnexoTextoView(View):

    def __init__(self):
        self.template_name = 'articulo/anexos/anexos_texto.html'

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            id_articulo = pk
            anexos = AnexoTexto.objects.filter(articulo=id_articulo)
            articulo = Articulo.objects.get(id=id_articulo)
            form = AnexoTextoForm()

            contexto = {
                'form': form,
                'id': id_articulo,
                'articulo': articulo,
                'anexos': anexos,
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        id_articulo = pk
        form = AnexoTextoForm(request.POST)
        anexos = AnexoTexto.objects.filter(articulo=id_articulo)
        articulo = Articulo.objects.get(id=id_articulo)

        if form.is_valid():
            texto = form.save(commit=False)
            texto.articulo_id = id_articulo
            texto.save()
            anexos = AnexoTexto.objects.filter(articulo=id_articulo)
            form = AnexoTextoForm()
        return render(request, 'articulo/anexos/anexos_texto.html',
                      {'form': form, 'id': id_articulo, 'anexos': anexos,
                       'articulo': articulo})


class ArticuloAnexoImagenView(View):

    def __init__(self):
        self.template_name = 'articulo/anexos/anexos_imagen.html'

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            id_articulo = pk
            anexos = AnexoImagen.objects.filter(articulo=id_articulo)
            articulo = Articulo.objects.get(id=id_articulo)
            form = AnexoImagenForm()

            contexto = {
                'form': form,
                'id': id_articulo,
                'articulo': articulo,
                'anexos': anexos,
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        id_articulo = pk
        anexos = AnexoImagen.objects.filter(articulo=id_articulo)
        articulo = Articulo.objects.get(id=id_articulo)
        form = AnexoImagenForm(request.POST, request.FILES)

        if form.is_valid():
            imagen_anexo = AnexoImagen()
            imagen_anexo.descripcion = request.POST['descripcion']
            if 'ruta' in request.POST:
                imagen_anexo.ruta = request.POST['ruta']
            else:
                imagen_anexo.ruta = request.FILES['ruta']
            imagen_anexo.articulo_id = id_articulo
            imagen_anexo.save()
            form = AnexoImagenForm()
            anexos = AnexoImagen.objects.filter(articulo=id_articulo)

        contexto = {
            'form': form,
            'id': id_articulo,
            'articulo': articulo,
            'anexos': anexos,
        }

        return render(request, self.template_name, contexto)


class ArticuloAnexoArchivoView(View):

    def __init__(self):
        self.template_name = 'articulo/anexos/anexos_archivo.html'

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            id_articulo = pk
            anexos = AnexoArchivo.objects.filter(articulo=id_articulo)
            articulo = Articulo.objects.get(id=id_articulo)
            form = AnexoArchivoForm()

            contexto = {
                'form': form,
                'id': id_articulo,
                'articulo': articulo,
                'anexos': anexos,
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        id_articulo = pk
        articulo = Articulo.objects.get(id=id_articulo)
        anexos = AnexoArchivo.objects.filter(articulo=id_articulo)
        form = AnexoArchivoForm(request.POST, request.FILES)

        if form.is_valid():
            archivo_anexo = AnexoArchivo()
            archivo_anexo.descripcion = request.POST['descripcion']
            if 'archivo' in request.POST:
                archivo_anexo.archivo = request.POST['archivo']
            else:
                archivo_anexo.archivo = request.FILES['archivo']
            archivo_anexo.articulo_id = id_articulo
            archivo_anexo.save()
            anexos = AnexoArchivo.objects.filter(articulo=id_articulo)
            form = AnexoArchivoForm()

            contexto = {
                'form': form,
                'id': id_articulo,
                'articulo': articulo,
                'anexos': anexos,
            }

            return render(request, self.template_name, contexto)


class ArticuloAnexoTextoAPI(viewsets.ModelViewSet):
    queryset = AnexoTexto.objects.all()
    serializer_class = AnexoTextoSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('articulo',)


class ArticuloAnexoImagenAPI(viewsets.ModelViewSet):
    queryset = AnexoImagen.objects.all()
    serializer_class = AnexoImagenSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('articulo',)


class ArticuloAnexoArchivoAPI(viewsets.ModelViewSet):
    queryset = AnexoArchivo.objects.all()
    serializer_class = AnexoArchivoSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('articulo',)


# ----------------- STOCK ----------------- #


class StockListView(View):
    template_name = 'stock/lista.html'

    def get(self, request, almacen, articulo):

        valores_iniciales = {}

        if almacen != 0:
            valores_iniciales['almacen'] = almacen

        if articulo != 0:
            valores_iniciales['articulo'] = articulo

        formulario = StockFilterForm(initial=valores_iniciales)

        contexto = {
            'form': formulario
        }

        return render(request, self.template_name, contexto)

    def post(self, request, almacen, articulo):
        return render(request, self.template_name, {})


class StockAPI(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    pagination_class = GenericPagination

    filter_backends = (DjangoFilterBackend,)
    filter_class = StockFilter


class StockExcelAPI(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = StockFilter


class MovimientoAPI(viewsets.ModelViewSet):
    queryset = MovimientoCabecera.objects.all().order_by('-created_date')
    serializer_class = MovimientoCabeceraSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = MovimientoCabeceraFilter


class MovimientoExcelAPI(viewsets.ModelViewSet):
    queryset = MovimientoCabecera.objects.all().order_by('-created_date')
    serializer_class = MovimientoCabeceraSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MovimientoCabeceraFilter


class MovimientoDetalleAPI(viewsets.ModelViewSet):
    queryset = MovimientoDetalle.objects.all().order_by('-created_date')
    serializer_class = MovimientoDetalleSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('cabecera',)


class MovimientoDetalleExcelAPI(viewsets.ModelViewSet):
    queryset = MovimientoDetalle.objects.all().order_by('-created_date')
    serializer_class = MovimientoDetalleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('cabecera',)


class MovimientoInventarioAPI(viewsets.ModelViewSet):
    queryset = MovimientoDetalle.objects.all().order_by('-created_date')
    serializer_class = MovimientoInventarioSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = MovimientoInventarioFilter


class MovimientoInventarioExcelAPI(viewsets.ModelViewSet):
    queryset = MovimientoDetalle.objects.all().order_by('-created_date')
    serializer_class = MovimientoInventarioSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MovimientoInventarioFilter


# ------------ MOVIMIENTOS AL ALMACEN ---------------- #


class MovimientoListView(View):

    def __init__(self):
        self.template_name = "movimiento/lista.html"

    def get(self, request):
        formulario = InventarioFiltersForm()

        contexto = {
            'form': formulario
        }

        return render(request, self.template_name, contexto)


class MovimientoDetailView(View):

    def __init__(self):
        self.template_name = "movimiento/detalle.html"

    def get(self, request, pk):
        cabecera = get_object_or_404(MovimientoCabecera, pk=pk)
        formulario = InventarioForm(instance=cabecera)

        contexto = {
            'form': formulario,
            'operation': 'Ver Detalle',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display(),
            'created_date': cabecera.created_date,
            'created_by': cabecera.created_by,
            'tipo': cabecera.get_tipo_display()
        }

        return render(request, self.template_name, contexto)


# ---------------  ENTRADAS --------------------- #


class EntradaSaldoListView(View):

    def __init__(self):
        self.template_name = 'entrada/saldo_inicial/lista.html'

    def get(self, request):

        formulario = EntradaSaldoFiltersForm()

        contexto = {
            'form': formulario
        }

        return render(request, self.template_name, contexto)


class EntradaSaldoCreateView(View):

    def __init__(self):
        self.template_name = "entrada/saldo_inicial/formulario.html"
        self.negocio = EntradaAlmacenBusiness()

    def get(self, request):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):
            formulario = EntradaSaldoForm()
            contexto = {
                'form': formulario,
                'operation': 'Nuevo',
                'id_cabecera': ''
            }

            return render(request, self.template_name, contexto)

        else:
            raise PermissionDenied

    def post(self, request):

        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = EntradaCompraForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraEntrada(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_LineasEntradaEnStock(cabecera)

            if resultado is not True:
                messages.add_message(
                    request,
                    messages.ERROR,
                    resultado
                )

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:entradas_saldoinicial_lista')
                )

        else:

            if id_cabecera:
                cabecera = get_object_or_404(
                    MovimientoCabecera,
                    pk=id_cabecera
                )
                formulario = EntradaSaldoForm(request.POST, instance=cabecera)
                self.negocio.actualizar_CabeceraEntrada(
                    cabecera,
                    formulario,
                    request.user.profile
                )
                id_cabecera = cabecera.pk

            else:
                formulario = EntradaSaldoForm(request.POST)
                cabecera = self.negocio.crear_CabeceraEntrada(
                    formulario,
                    request.user.profile,
                    'SAL'
                )
                if cabecera:

                    id_cabecera = cabecera.pk
                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                        'id_cabecera': id_cabecera,
                        'estado_cabecera': cabecera.get_estado_display()
                    }
                    return render(request, self.template_name, contexto)
                else:

                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                    }
                    return render(request, self.template_name, contexto)

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display()
        }

        return render(request, self.template_name, contexto)


class EntradaSaldoUpdateView(View):
    def __init__(self):
        self.template_name = 'entrada/saldo_inicial/formulario.html'
        self.negocio = EntradaAlmacenBusiness()

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            cabecera = get_object_or_404(MovimientoCabecera, pk=pk)
            formulario = EntradaSaldoForm(instance=cabecera)

            contexto = {
                'form': formulario,
                'operation': 'Editar',
                'id_cabecera': cabecera.pk,
                'estado_cabecera': cabecera.get_estado_display(),
                'created_date': cabecera.created_date,
                'created_by': cabecera.created_by
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):

        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = EntradaSaldoForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraEntrada(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_LineasEntradaEnStock(cabecera)

            if resultado is not True:
                messages.add_message(
                    request,
                    messages.ERROR,
                    resultado
                )

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:entradas_saldoinicial_lista')
                )

        else:

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = EntradaSaldoForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraEntrada(
                cabecera,
                formulario,
                request.user.profile
            )

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': id_cabecera,
            'estado_cabecera': cabecera.get_estado_display()
        }

        return render(request, self.template_name, contexto)


class EntradaCompraListView(View):
    def __init__(self):
        self.template_name = "entrada/compra/lista.html"

    def get(self, request):
        formulario = EntradaCompraFiltersForm()
        contexto = {
            'form': formulario,
        }

        return render(request, self.template_name, contexto)


class EntradaCompraCreateView(View):

    def __init__(self):
        self.template_name = "entrada/compra/formulario.html"
        self.negocio = EntradaAlmacenBusiness()

    def get(self, request):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            formulario = EntradaCompraForm(
                initial={
                    'persona_recibe': request.user
                }
            )
            contexto = {
                'form': formulario,
                'operation': 'Nuevo',
                'id_cabecera': ''
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request):

        # Se obtiene valor del id de la cabecera
        id_cabecera = request.POST.get('id_cabecera')

        # Se obtiene el boton que lanza el evento
        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        # Se determina la accion a tomar de acuerdo el boton:
        if boton == "finalizar":

            # Actualiza Cabecera
            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = EntradaCompraForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraEntrada(
                cabecera,
                formulario,
                request.user.profile
            )

            # Afecta Inventario:
            resultado = self.negocio.guardar_LineasEntradaEnStock(cabecera)

            if resultado is not True:
                messages.add_message(
                    request,
                    messages.ERROR,
                    resultado
                )

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:entradas_compras_lista')
                )
        else:

            # Actualiza el Cabecera
            if id_cabecera:
                cabecera = get_object_or_404(
                    MovimientoCabecera,
                    pk=id_cabecera
                )
                formulario = EntradaCompraForm(request.POST, instance=cabecera)
                self.negocio.actualizar_CabeceraEntrada(
                    cabecera,
                    formulario,
                    request.user.profile
                )

            # Crea Cabecera
            else:
                formulario = EntradaCompraForm(request.POST)
                cabecera = self.negocio.crear_CabeceraEntrada(
                    formulario,
                    request.user.profile,
                    'COM'
                )
                if cabecera:

                    id_cabecera = cabecera.pk
                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                        'id_cabecera': id_cabecera,
                        'estado_cabecera': cabecera.get_estado_display()
                    }
                    return render(request, self.template_name, contexto)
                else:

                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                    }
                    return render(request, self.template_name, contexto)

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display()
        }

        return render(request, self.template_name, contexto)


class EntradaCompraUpdateView(View):

    def __init__(self):
        self.template_name = "entrada/compra/formulario.html"
        self.negocio = EntradaAlmacenBusiness()

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            cabecera = get_object_or_404(
                MovimientoCabecera,
                pk=pk
            )

            formulario = EntradaCompraForm(instance=cabecera)

            contexto = {
                'form': formulario,
                'operation': 'Editar',
                'id_cabecera': cabecera.pk,
                'estado_cabecera': cabecera.get_estado_display(),
                'created_date': cabecera.created_date,
                'created_by': cabecera.created_by
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):

        # Se obtiene valor del id de la cabecera
        id_cabecera = request.POST.get('id_cabecera')

        # Se obtiene el boton que lanza el evento
        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        # Se determina la accion a tomar de acuerdo el boton:
        if boton == "finalizar":

            # Actualiza Cabecera
            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = EntradaCompraForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraEntrada(
                cabecera,
                formulario,
                request.user.profile
            )

            # Afecta Inventario:
            resultado = self.negocio.guardar_LineasEntradaEnStock(cabecera)

            if resultado is not True:
                messages.add_message(
                    request,
                    messages.ERROR,
                    resultado
                )

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:entradas_compras_lista')
                )
        else:

            # Actualiza el Cabecera
            cabecera = get_object_or_404(
                MovimientoCabecera,
                pk=id_cabecera
            )
            formulario = EntradaCompraForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraEntrada(
                cabecera,
                formulario,
                request.user.profile
            )

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': id_cabecera,
            'estado_cabecera': cabecera.get_estado_display(),
            'created_date': cabecera.created_date,
            'created_by': cabecera.created_by
        }

        return render(request, self.template_name, contexto)


class EntradaAjusteListView(View):

    def __init__(self):
        self.template_name = "entrada/ajuste/lista.html"

    def get(self, request):
        formulario = EntradaAjusteFiltersForm()

        contexto = {
            'form': formulario,
        }

        return render(request, self.template_name, contexto)


class EntradaAjusteCreateView(View):

    def __init__(self):
        self.template_name = "entrada/ajuste/formulario.html"
        self.negocio = EntradaAlmacenBusiness()

    def get(self, request):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            formulario = EntradaAjusteForm()
            contexto = {
                'form': formulario,
                'operation': 'Nuevo',
                'id_cabecera': ''
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request):

        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == 'finalizar':

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = EntradaAjusteForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraEntrada(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_LineasEntradaEnStock(cabecera)

            if resultado is not True:
                messages.add_message(
                    request,
                    messages.ERROR,
                    resultado
                )

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:entradas_ajustes_lista')
                )
        else:
            formulario = EntradaAjusteForm(request.POST)
            cabecera = self.negocio.crear_CabeceraEntrada(
                formulario,
                request.user.profile,
                'AJU'
            )
            if cabecera:

                    id_cabecera = cabecera.pk
                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                        'id_cabecera': id_cabecera,
                        'estado_cabecera': cabecera.get_estado_display()
                    }
                    return render(request, self.template_name, contexto)
            else:

                contexto = {
                    'form': formulario,
                    'operation': 'Nuevo',
                }
                return render(request, self.template_name, contexto)

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display()
        }

        return render(request, self.template_name, contexto)


class EntradaAjusteUpdateView(View):

    def __init__(self):
        self.template_name = "entrada/ajuste/formulario.html"
        self.negocio = EntradaAlmacenBusiness()

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            cabecera = get_object_or_404(MovimientoCabecera, pk=pk)
            formulario = EntradaAjusteForm(instance=cabecera)

            contexto = {
                'form': formulario,
                'operation': 'Editar',
                'id_cabecera': cabecera.pk,
                'estado_cabecera': cabecera.get_estado_display(),
                'created_date': cabecera.created_date,
                'created_by': cabecera.created_by
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = EntradaAjusteForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraEntrada(cabecera, formulario, request.user.profile)

            resultado = self.negocio.guardar_LineasEntradaEnStock(cabecera)

            if resultado is not True:
                messages.add_message(
                    request,
                    messages.ERROR,
                    resultado
                )

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:entradas_ajustes_lista')
                )

        else:

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = EntradaAjusteForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraEntrada(
                cabecera,
                formulario,
                request.user.profile
            )

        contexto = {
            'form': formulario,
            'operation': 'Editar',
            'id_cabecera': id_cabecera,
            'estado_cabecera': cabecera.get_estado_display(),
            'created_date': cabecera.created_date,
            'created_by': cabecera.created_by
        }

        return render(request, self.template_name, contexto)


class EntradaTraspasoListView(View):

    def __init__(self):
        self.template_name = "entrada/traspaso/lista.html"

    def get(self, request, estado=None):

        formulario = EntradaTraspasoFiltersForm(initial={'estado': estado})

        contexto = {
            'form': formulario
        }

        return render(request, self.template_name, contexto)


class EntradaTraspasoDetailView(View):

    def __init__(self):
        self.template_name = "entrada/traspaso/detalle.html"

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            cabecera = get_object_or_404(MovimientoCabecera, pk=pk)
            formulario = SalidaTraspasoForm(instance=cabecera)

            contexto = {
                'form': formulario,
                'estado_cabecera': cabecera.get_estado_display(),
                'id_cabecera': cabecera.pk,
                'operation': 'Ver Detalle'
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied


class EntradaTransitoListView(View):

    def __init__(self):
        self.template_name = "entrada/transito/lista.html"

    def get(self, request):
        formulario = SalidaTraspasoFiltersForm

        contexto = {
            'form': formulario
        }

        return render(request, self.template_name, contexto)


class EntradaTransitoReceiveView(View):

    def __init__(self):
        self.template_name = "entrada/traspaso/detalle.html"
        self.negocio = TraspasoBusiness()

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            cabecera = get_object_or_404(MovimientoCabecera, pk=pk)
            formulario = SalidaTraspasoForm(instance=cabecera)

            contexto = {
                'form': formulario,
                'operation': 'Detalle',
                'id_cabecera': cabecera.pk,
                'estado_cabecera': cabecera.get_estado_display()
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        entrada = get_object_or_404(MovimientoCabecera, pk=pk)
        stock_afectado = self.negocio.guardar_LineasEntradaTraspasoEnStock(
            entrada
        )
        if stock_afectado == "Exito":
            traspaso_cerrado = self.negocio.cerrar_Traspaso(
                entrada,
                request.user.profile
            )
            if traspaso_cerrado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Exito"
                )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                stock_afectado
            )

        return redirect(reverse(
            'inventarios:entradas_traspaso_lista')
        )


# ------------------   SALIDAS    ------------------------ #

class SalidaPersonalListView(View):

    def __init__(self):
        self.template_name = "salida/personal/lista.html"

    def get(self, request):
        formulario = SalidaPersonalFiltersForm()
        contexto = {
            'form': formulario,
        }
        return render(request, self.template_name, contexto)


class SalidaPersonalCreateView(View):

    def __init__(self):
        self.template_name = "salida/personal/formulario.html"
        self.negocio = SalidaAlmacenBusiness()

    def get(self, request):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            formulario = SalidaPersonalForm(
                initial={
                    'persona_entrega': request.user
                }
            )

            contexto = {
                'form': formulario,
                'operation': 'Nuevo',
                'id_cabecera': ''
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request):

        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaPersonalForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraSalida(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_LineasSalidaEnStock(cabecera)

            if resultado is not True:
                id_cabecera = cabecera.pk
                contexto = {
                    'form': formulario,
                    'operation': 'Nuevo',
                    'id_cabecera': id_cabecera,
                    'estado_cabecera': cabecera.get_estado_display(),
                    'errores': resultado
                }
                return render(request, self.template_name, contexto)

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:salidas_personal_lista')
                )
        else:

            if id_cabecera:
                cabecera = get_object_or_404(
                    MovimientoCabecera,
                    pk=id_cabecera
                )
                formulario = SalidaPersonalForm(request.POST,
                                                instance=cabecera)
                self.negocio.actualizar_CabeceraSalida(
                    cabecera,
                    formulario,
                    request.user.profile
                )

            else:
                formulario = SalidaPersonalForm(request.POST)
                cabecera = self.negocio.crear_CabeceraSalida(
                    formulario,
                    request.user.profile,
                    'DES'
                )
                if cabecera:

                    id_cabecera = cabecera.pk
                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                        'id_cabecera': id_cabecera,
                        'estado_cabecera': cabecera.get_estado_display()
                    }
                    return render(request, self.template_name, contexto)
                else:

                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                    }
                    return render(request, self.template_name, contexto)

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display()
        }

        return render(request, self.template_name, contexto)


class SalidaPersonalUpdateView(View):

    def __init__(self):
        self.template_name = "salida/personal/formulario.html"
        self.negocio = SalidaAlmacenBusiness()

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            cabecera = get_object_or_404(MovimientoCabecera, pk=pk)
            formulario = SalidaPersonalForm(instance=cabecera)

            contexto = {
                'form': formulario,
                'operation': 'Editar',
                'id_cabecera': cabecera.pk,
                'estado_cabecera': cabecera.get_estado_display(),
                'created_date': cabecera.created_date,
                'created_by': cabecera.created_by
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaPersonalForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraSalida(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_LineasSalidaEnStock(cabecera)

            if resultado is not True:
                id_cabecera = cabecera.pk
                contexto = {
                    'form': formulario,
                    'operation': 'Nuevo',
                    'id_cabecera': id_cabecera,
                    'estado_cabecera': cabecera.get_estado_display(),
                    'errores': resultado
                }
                return render(request, self.template_name, contexto)

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:salidas_personal_lista')
                )
        else:

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaPersonalForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraSalida(
                cabecera,
                formulario,
                request.user.profile
            )

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': id_cabecera,
            'estado_cabecera': cabecera.get_estado_display(),
            'created_date': cabecera.created_date,
            'created_by': cabecera.created_by
        }

        return render(request, self.template_name, contexto)


class SalidaOrdenTrabajoListView(View):

    def __init__(self):
        self.template_name = "salida/orden_trabajo/lista.html"

    def get(self, request):
        formulario = SalidaOrdenTrabajoFiltersForm()

        contexto = {
            'form': formulario,
        }

        return render(request, self.template_name, contexto)


class SalidaOrdenTrabajoCreateView(View):

    def __init__(self):
        self.template_name = "salida/orden_trabajo/formulario.html"
        self.negocio = SalidaOrdenTrabajoBusiness()

    def get(self, request):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            formulario = SalidaOrdenTrabajoForm(
                initial={
                    'persona_entrega': request.user
                }
            )

            contexto = {
                'form': formulario,
                'operation': 'Nuevo',
                'id_cabecera': ''
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request):

        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaOrdenTrabajoForm(
                request.POST, instance=cabecera)
            self.negocio.actualizar_Cabecera(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_Lineas(cabecera)

            if resultado is not True:
                id_cabecera = cabecera.pk
                contexto = {
                    'form': formulario,
                    'operation': 'Nuevo',
                    'id_cabecera': id_cabecera,
                    'estado_cabecera': cabecera.get_estado_display(),
                    'errores': resultado
                }
                return render(request, self.template_name, contexto)

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:salidas_ordentrabajo_lista')
                )
        else:

            # Actualiza registro
            if id_cabecera:

                cabecera = get_object_or_404(
                    MovimientoCabecera,
                    pk=id_cabecera
                )
                formulario = SalidaOrdenTrabajoForm(
                    request.POST, instance=cabecera)
                self.negocio.actualizar_Cabecera(
                    cabecera,
                    formulario,
                    request.user.profile
                )

            # Crea registro
            else:
                formulario = SalidaOrdenTrabajoForm(request.POST)
                cabecera = self.negocio.crear_Cabecera(
                    formulario,
                    request.user.profile
                )
                if cabecera:

                    id_cabecera = cabecera.pk
                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                        'id_cabecera': id_cabecera,
                        'estado_cabecera': cabecera.get_estado_display()
                    }
                    return render(request, self.template_name, contexto)
                else:

                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                    }
                    return render(request, self.template_name, contexto)

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display()
        }

        return render(request, self.template_name, contexto)


class SalidaOrdenTrabajoUpdateView(View):

    def __init__(self):
        self.template_name = "salida/orden_trabajo/formulario.html"
        self.negocio = SalidaOrdenTrabajoBusiness()

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            cabecera = get_object_or_404(MovimientoCabecera, pk=pk)
            formulario = SalidaOrdenTrabajoForm(instance=cabecera)

            contexto = {
                'form': formulario,
                'operation': 'Editar',
                'id_cabecera': cabecera.pk,
                'estado_cabecera': cabecera.get_estado_display(),
                'created_date': cabecera.created_date,
                'created_by': cabecera.created_by
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):

        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaOrdenTrabajoForm(request.POST,
                                                instance=cabecera)
            self.negocio.actualizar_Cabecera(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_Lineas(cabecera)

            if resultado is not True:
                id_cabecera = cabecera.pk
                contexto = {
                    'form': formulario,
                    'operation': 'Nuevo',
                    'id_cabecera': id_cabecera,
                    'estado_cabecera': cabecera.get_estado_display(),
                    'errores': resultado
                }
                return render(request, self.template_name, contexto)

            else:

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:salidas_ordentrabajo_lista')
                )

        else:

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaOrdenTrabajoForm(request.POST,
                                                instance=cabecera)
            self.negocio.actualizar_Cabecera(
                cabecera,
                formulario,
                request.user.profile
            )

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': id_cabecera,
            'estado_cabecera': cabecera.get_estado_display(),
            'created_date': cabecera.created_date,
            'created_by': cabecera.created_by
        }

        return render(request, self.template_name, contexto)


class SalidaAjusteListView(View):

    def __init__(self):
        self.template_name = "salida/ajuste/lista.html"

    def get(self, request):
        formulario = SalidaAjusteFiltersForm()

        contexto = {
            'form': formulario,
        }

        return render(request, self.template_name, contexto)


class SalidaAjusteCreateView(View):

    def __init__(self):
        self.template_name = "salida/ajuste/formulario.html"
        self.negocio = SalidaAlmacenBusiness()

    def get(self, request):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            formulario = SalidaAjusteForm()
            contexto = {
                'form': formulario,
                'operation': 'Nuevo',
                'id_cabecera': ''
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request):

        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaAjusteForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraSalida(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_LineasSalidaEnStock(cabecera)

            if resultado is not True:
                id_cabecera = cabecera.pk
                contexto = {
                    'form': formulario,
                    'operation': 'Nuevo',
                    'id_cabecera': id_cabecera,
                    'estado_cabecera': cabecera.get_estado_display(),
                    'errores': resultado
                }
                return render(request, self.template_name, contexto)

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:salidas_ajustes_lista')
                )

        else:

            if id_cabecera:
                cabecera = get_object_or_404(
                    MovimientoCabecera,
                    pk=id_cabecera
                )
                formulario = SalidaAjusteForm(request.POST,
                                              instance=cabecera)
                self.negocio.actualizar_CabeceraSalida(
                    cabecera,
                    formulario,
                    request.user.profile
                )

            else:
                formulario = SalidaAjusteForm(request.POST)
                cabecera = self.negocio.crear_CabeceraSalida(
                    formulario,
                    request.user.profile,
                    'AJU'
                )
                if cabecera:

                    id_cabecera = cabecera.pk
                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                        'id_cabecera': id_cabecera,
                        'estado_cabecera': cabecera.get_estado_display()
                    }
                    return render(request, self.template_name, contexto)
                else:

                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                    }
                    return render(request, self.template_name, contexto)

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display()
        }

        return render(request, self.template_name, contexto)


class SalidaAjusteUpdateView(View):

    def __init__(self):
        self.template_name = "salida/ajuste/formulario.html"
        self.negocio = SalidaAlmacenBusiness()

    def get(self, request, pk):

        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            cabecera = get_object_or_404(MovimientoCabecera, pk=pk)
            formulario = SalidaAjusteForm(instance=cabecera)

            contexto = {
                'form': formulario,
                'operation': 'Editar',
                'id_cabecera': cabecera.pk,
                'estado_cabecera': cabecera.get_estado_display(),
                'created_date': cabecera.created_date,
                'created_by': cabecera.created_by
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaAjusteForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraSalida(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_LineasSalidaEnStock(cabecera)

            if resultado is not True:
                id_cabecera = cabecera.pk
                contexto = {
                    'form': formulario,
                    'operation': 'Nuevo',
                    'id_cabecera': id_cabecera,
                    'estado_cabecera': cabecera.get_estado_display(),
                    'errores': resultado
                }
                return render(request, self.template_name, contexto)

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                return redirect(reverse(
                    'inventarios:salidas_ajustes_lista')
                )

        else:

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaPersonalForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraSalida(
                cabecera,
                formulario,
                request.user.profile
            )

        contexto = {
            'form': formulario,
            'operation': 'Editar',
            'id_cabecera': id_cabecera,
            'estado_cabecera': cabecera.get_estado_display(),
            'created_date': cabecera.created_date,
            'created_by': cabecera.created_by
        }

        return render(request, self.template_name, contexto)


class SalidaTraspasoListView(View):

    def __init__(self):
        self.template_name = "salida/traspaso/lista.html"

    def get(self, request):

        formulario = SalidaTraspasoFiltersForm()

        contexto = {
            'form': formulario
        }

        return render(request, self.template_name, contexto)


class SalidaTraspasoCreateView(View):

    def __init__(self):
        self.template_name = "salida/traspaso/formulario.html"
        self.negocio = TraspasoBusiness()

    def get(self, request):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            formulario = SalidaTraspasoForm()

            contexto = {
                'form': formulario,
                'operation': 'Nuevo'
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request):

        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaTraspasoForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraTraspaso(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_LineasSalidaTraspasoEnStock(cabecera)

            if resultado is not True:
                id_cabecera = cabecera.pk
                contexto = {
                    'form': formulario,
                    'operation': 'Nuevo',
                    'id_cabecera': id_cabecera,
                    'estado_cabecera': cabecera.get_estado_display(),
                    'errores': resultado
                }
                return render(request, self.template_name, contexto)

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )

                # SE CREA EL MOVIMIENTO DE LA ENTRADA DEL TRASPASO
                entrada = self.negocio.crear_CabeceraEntradaTraspaso(cabecera)
                print entrada
                detalles = self.negocio.crear_LineasDetalleEntradaTraspaso(
                    cabecera,
                    entrada
                )
                return redirect(reverse(
                    'inventarios:salidas_traspaso_lista')
                )

        else:

            if id_cabecera:
                cabecera = get_object_or_404(
                    MovimientoCabecera,
                    pk=id_cabecera
                )
                formulario = SalidaTraspasoForm(request.POST,
                                                instance=cabecera)
                self.negocio.actualizar_CabeceraTraspaso(
                    cabecera,
                    formulario,
                    request.user.profile
                )

            else:
                formulario = SalidaTraspasoForm(request.POST)
                cabecera = self.negocio.crear_CabeceraTraspaso(
                    formulario,
                    request.user.profile,
                    'TRA'
                )
                if cabecera:

                    id_cabecera = cabecera.pk
                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                        'id_cabecera': id_cabecera,
                        'estado_cabecera': cabecera.get_estado_display()
                    }
                    return render(request, self.template_name, contexto)
                else:

                    contexto = {
                        'form': formulario,
                        'operation': 'Nuevo',
                    }
                    return render(request, self.template_name, contexto)

        contexto = {
            'form': formulario,
            'operation': 'Nuevo',
            'id_cabecera': cabecera.pk,
            'estado_cabecera': cabecera.get_estado_display()
        }

        return render(request, self.template_name, contexto)


class SalidaTraspasoUpdateView(View):
    def __init__(self):
        self.template_name = "salida/traspaso/formulario.html"
        self.negocio = TraspasoBusiness()

    def get(self, request, pk):
        if request.user.is_staff or request.user.groups.filter(name='almacenista'):

            cabecera = get_object_or_404(MovimientoCabecera, pk=pk)
            formulario = SalidaTraspasoForm(instance=cabecera)

            contexto = {
                'form': formulario,
                'operation': 'Editar',
                'id_cabecera': cabecera.pk,
                'estado_cabecera': cabecera.get_estado_display(),
                'created_date': cabecera.created_date,
                'created_by': cabecera.created_by
            }

            return render(request, self.template_name, contexto)
        else:
            raise PermissionDenied

    def post(self, request, pk):
        id_cabecera = request.POST.get('id_cabecera')

        if request.POST.get('finalizar'):
            boton = request.POST.get('finalizar')
        else:
            boton = request.POST.get('guardar')

        if boton == "finalizar":

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaTraspasoForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraTraspaso(
                cabecera,
                formulario,
                request.user.profile
            )

            resultado = self.negocio.guardar_LineasSalidaTraspasoEnStock(cabecera)

            if resultado is not True:
                id_cabecera = cabecera.pk
                contexto = {
                    'form': formulario,
                    'operation': 'Nuevo',
                    'id_cabecera': id_cabecera,
                    'estado_cabecera': cabecera.get_estado_display(),
                    'errores': resultado
                }
                return render(request, self.template_name, contexto)

            elif resultado:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Se finalizó movimiento correctamente'
                )
                # SE CREA EL MOVIMIENTO DE LA ENTRADA DEL TRASPASO
                entrada = self.negocio.crear_CabeceraEntradaTraspaso(cabecera)
                print entrada
                detalles = self.negocio.crear_LineasDetalleEntradaTraspaso(
                    cabecera,
                    entrada
                )
                return redirect(reverse(
                    'inventarios:salidas_traspaso_lista')
                )

        else:

            cabecera = get_object_or_404(MovimientoCabecera, pk=id_cabecera)
            formulario = SalidaTraspasoForm(request.POST, instance=cabecera)
            self.negocio.actualizar_CabeceraTraspaso(
                cabecera,
                formulario,
                request.user.profile
            )

        contexto = {
            'form': formulario,
            'operation': 'Editar',
            'id_cabecera': id_cabecera,
            'estado_cabecera': cabecera.get_estado_display(),
            'created_date': cabecera.created_date,
            'created_by': cabecera.created_by
        }

        return render(request, self.template_name, contexto)


class EntradaTransitoCountAPI(APIView):

    def get(self, request, format=None):
        total = MovimientoCabecera.objects.filter(
            tipo="ENT").filter(estado="TRAN").count()
        data = {'data': total}
        return Response(data)
