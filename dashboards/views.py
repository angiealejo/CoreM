# -*- coding: utf-8 -*-

# Librerias django:

# Django Atajos
from django.shortcuts import render

# Django Login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Django Generic Views
from django.views.generic.base import View


@method_decorator(login_required, name='dispatch')
class Inicio(View):

    def __init__(self):
        self.template_name = 'inicio.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        return render(request, self.template_name, {})
