# -*- coding: utf-8 -*-

# Librerias django

# Django Atajos
from django.shortcuts import render

# Django Generic Views
from django.views.generic.base import View
from django.views.generic import TemplateView


class Index(View):

    def __init__(self):
        self.template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        return render(request, self.template_name, {})


# ----------------- PANTALLA DE ERROR ----------------- #

class Error(TemplateView):
    template_name = '500.html'
