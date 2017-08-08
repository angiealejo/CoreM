# -*- coding: utf-8 -*-


# Librerias Python
import os
from io import BytesIO

# Librerias Django
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings

# Librerias Terceros
from xhtml2pdf import pisa


def get_ImagePath(instance, filename):
    if (instance.equipo_id):
        upload_dir = os.path.join(
            'equipos', instance.equipo_id, 'anexos', 'img')

    elif (instance.articulo_id):
        upload_dir = os.path.join(
            'articulos', instance.articulo_id, 'anexos', 'img')

    elif (instance.orden_trabajo_id):
        upload_dir = os.path.join(
            'ordenes', instance.orden_trabajo_id, 'anexos', 'img')
    return os.path.join(upload_dir, filename)


def get_FilePath(instance, filename):
    if (instance.equipo_id):
        upload_dir = os.path.join(
            'equipos', instance.equipo_id, 'anexos', 'files')

    elif (instance.articulo_id):
        upload_dir = os.path.join(
            'articulos', instance.articulo_id, 'anexos', 'files')

    elif (instance.orden_trabajo_id):
        upload_dir = os.path.join(
            'ordenes', instance.orden_trabajo_id, 'anexos', 'files')
    return os.path.join(upload_dir, filename)


class UnsupportedMediaPathException(Exception):
    pass


def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))

        if not os.path.isfile(path):
            path = os.path.join(settings.MEDIA_ROOT,
                                uri.replace(settings.MEDIA_URL, ""))

            if not os.path.isfile(path):
                raise UnsupportedMediaPathException(
                    'media urls must start with %s or %s' % (
                        settings.MEDIA_ROOT, settings.STATIC_ROOT))

    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
