# coding: utf-8
from .models import SolicitudCompraEncabezado


class SolicitudCompraBusiness(object):

    def crear_CabeceraSolicitud(self, formulario, usuario):

        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            cabecera = SolicitudCompraEncabezado()
            cabecera.descripcion = datos_formulario.get('descripcion')
            cabecera.comentarios = datos_formulario.get('comentarios')
            cabecera.solicitante = datos_formulario.get('solicitante')
            cabecera.created_by = usuario
            cabecera.save()

            return cabecera

    def actualizar_CabeceraSolicitud(self, cabecera, formulario, usuario):
        if cabecera.estado != "CER":
            if formulario.is_valid():
                cabecera = formulario.save(commit=False)
                cabecera.updated_by = usuario
                cabecera.save()

                return cabecera

    def validar_LineasDetalle(self, cabecera):

        # Se valida el estado de la cabecera:
        if cabecera.estado != "CER":

            lineas_detalle = cabecera.solicitudcompradetalle_set.all()

            # Se valida que se tenga al menos una linea
            if len(lineas_detalle) > 0:

                cabecera.estado = "CER"
                cabecera.save()

                return True

            else:
                return "El detalle no tiene lineas"

        else:
            return "El movimiento ya está cerrado"
