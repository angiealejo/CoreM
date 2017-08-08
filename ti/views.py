# -*- coding: utf-8 -*-

# Librerias django

# Django Atajos
from django.shortcuts import render

# Django Seguridad:
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Django Generic Views
from django.views.generic.base import View

# Otros modelos:
from inventarios.models import Articulo
from inventarios.models import Stock
from inventarios.models import Almacen


@method_decorator(login_required, name='dispatch')
class FixAlmacenView(View):

    def __init__(self):
        self.template_name = 'fix_almacen.html'
        self.clave_almacen = "ALM-001-TIERRA"

    def get(self, request):

        # obtener todos los articulos
        articulos = Articulo.objects.all()
        almacen = Almacen.objects.get(clave=self.clave_almacen)

        registros = []

        # recorrer cada articulo:
        for articulo in articulos:

            # buscar que tenga stock en tierra
            stock_tierra = Stock.objects.filter(
                articulo=articulo,
                almacen=almacen
            )

            # Si no tiene stock en tierra:
            if len(stock_tierra) == 0:

                # Agregar al contexto:
                registros.append(articulo)

        contexto = {
            'registros': registros
        }

        return render(request, self.template_name, contexto)

    def post(self, request):

        # obtener todos los articulos
        articulos = Articulo.objects.all()
        almacen = Almacen.objects.get(clave=self.clave_almacen)

        registros = []

        # recorrer cada articulo:
        for articulo in articulos:

            # buscar que tenga stock en tierra
            stock_tierra = Stock.objects.filter(
                articulo=articulo,
                almacen=almacen
            )

            # Si no tiene stock en tierra:
            if len(stock_tierra) == 0:

                # Agregar al contexto:
                registros.append(articulo)

                # Crear el stock
                stock = Stock()
                stock.almacen = almacen
                stock.articulo = articulo
                stock.cantidad = 0.0
                stock.save()

        contexto = {
            'registros': registros
        }

        return render(request, self.template_name, contexto)
