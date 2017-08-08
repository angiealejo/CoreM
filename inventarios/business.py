# coding: utf-8
from .models import MovimientoCabecera
from .models import MovimientoDetalle
from .models import Stock

# from trabajos.models import OrdenTrabajo
from trabajos.models import Material


class EntradaAlmacenBusiness(object):

    def __init__(self):
        self.tipo = "ENT"

    def crear_CabeceraEntrada(self, formulario, usuario, clase):

        # si la clase es COMPRA
        if clase == "COM":
            if formulario.is_valid():
                datos_formulario = formulario.cleaned_data
                cabecera = MovimientoCabecera()
                cabecera.descripcion = datos_formulario.get('descripcion')
                cabecera.fecha = datos_formulario.get('fecha')
                cabecera.almacen_destino = datos_formulario.get(
                    'almacen_destino'
                )
                cabecera.proveedor = datos_formulario.get('proveedor')

                cabecera.persona_recibe = datos_formulario.get(
                    'persona_recibe'
                )
                cabecera.created_by = usuario
                cabecera.tipo = self.tipo
                cabecera.clasificacion = clase
                cabecera.save()

                return cabecera

        # si la clase es AJUSTE o SALDO INICIAL
        elif clase == "AJU" or clase == "SAL":
            if formulario.is_valid():
                datos_formulario = formulario.cleaned_data
                cabecera = MovimientoCabecera()
                cabecera.descripcion = datos_formulario.get('descripcion')
                cabecera.fecha = datos_formulario.get('fecha')
                cabecera.almacen_destino = datos_formulario.get(
                    'almacen_destino'
                )
                cabecera.created_by = usuario
                cabecera.tipo = self.tipo
                cabecera.clasificacion = clase
                cabecera.save()

                return cabecera

    def actualizar_CabeceraEntrada(self, cabecera, formulario, usuario):
        if cabecera.estado != "CER":
            if formulario.is_valid():
                cabecera = formulario.save(commit=False)
                cabecera.updated_by = usuario
                cabecera.save()

    def guardar_LineasEntradaEnStock(self, cabecera):

        # Se valida el estado de la cabecera:
        if cabecera.estado != "CER":

            lineas_detalle = cabecera.movimientodetalle_set.all()

            # Se valida que se tenga al menos una linea
            if len(lineas_detalle) > 0:

                # Recorriendo lineas
                for linea in lineas_detalle:

                    # Registro Existe
                    fila_stock = Stock.objects.filter(
                        almacen=cabecera.almacen_destino,
                        articulo=linea.articulo
                    )

                    if fila_stock:

                        fila_stock[0].cantidad = fila_stock[
                            0].cantidad + linea.cantidad
                        fila_stock[0].save()

                    # Registro No Existe
                    else:

                        # Se crea el registro
                        Stock.objects.create(
                            almacen=cabecera.almacen_destino,
                            articulo=linea.articulo,
                            cantidad=linea.cantidad
                        )

                cabecera.estado = "CER"
                cabecera.save()

                return True

            else:
                return "El detalle no tiene lineas"

        else:
            return "El movimiento ya está cerrado"


class SalidaAlmacenBusiness(object):

    def __init__(self):
        self.tipo = "SAL"

    def crear_CabeceraSalida(self, formulario, usuario, clase):

        # si la clase es DESPACHO A PERSONAL
        if clase == "DES":
            if formulario.is_valid():
                datos_formulario = formulario.cleaned_data
                cabecera = MovimientoCabecera()
                cabecera.descripcion = datos_formulario.get('descripcion')
                cabecera.fecha = datos_formulario.get('fecha')
                cabecera.almacen_origen = datos_formulario.get(
                    'almacen_origen'
                )
                cabecera.persona_entrega = datos_formulario.get(
                    'persona_entrega'
                )
                cabecera.persona_recibe = datos_formulario.get(
                    'persona_recibe'
                )
                cabecera.created_by = usuario
                cabecera.tipo = self.tipo
                cabecera.clasificacion = clase
                cabecera.save()
                return cabecera

        # si la clase es AJUSTE
        elif clase == "AJU":
            if formulario.is_valid():
                datos_formulario = formulario.cleaned_data
                cabecera = MovimientoCabecera()
                cabecera.descripcion = datos_formulario.get('descripcion')
                cabecera.fecha = datos_formulario.get('fecha')
                cabecera.almacen_origen = datos_formulario.get(
                    'almacen_origen'
                )
                cabecera.created_by = usuario
                cabecera.tipo = self.tipo
                cabecera.clasificacion = clase
                cabecera.save()
                return cabecera

    def actualizar_CabeceraSalida(self, cabecera, formulario, usuario):
        if cabecera.estado != "CER":

            if formulario.is_valid():
                cabecera = formulario.save(commit=False)
                cabecera.updated_by = usuario
                cabecera.save()

    def guardar_LineasSalidaEnStock(self, cabecera):

        # Se valida el estado de la cabecera:
        if cabecera.estado != "CER":

            lineas_detalle = cabecera.movimientodetalle_set.all()
            errores = []
            # Se valida que se tenga al menos una linea
            if len(lineas_detalle) > 0:
                # contador = len(lineas_detalle)

                # Recorriendo lineas
                # while lineas_detalle > contador:
                for linea in lineas_detalle:

                    # Registro Existe
                    fila_stock = Stock.objects.filter(
                        almacen=cabecera.almacen_origen,
                        articulo=linea.articulo
                    )

                    if fila_stock:

                        if fila_stock[0].cantidad < linea.cantidad:

                            # return "No hay articulos suficientes"
                            error = "%s %s. %s %s" % (
                                "No hay articulos suficientes en almacen: ",
                                fila_stock[0].articulo,
                                ",Su cantidad actual es:",
                                fila_stock[0].cantidad)
                            errores.append(error)
                        else:
                            fila_stock[0].cantidad = fila_stock[
                                0].cantidad - linea.cantidad
                            fila_stock[0].save()

                    # Registro No Existe
                    else:
                        error = "%s: %s." % (
                            "No existe articulo registrado en almacen ",
                            linea.articulo)
                        errores.append(error)
                        # return errores
                        # return "No existe articulo registrado en Stock"
                # contador = contador + 1

                if len(errores) > 0:

                    return errores
                else:
                    cabecera.estado = "CER"
                    cabecera.save()
                    return True

            else:
                error = "%s" % ("El detalle no tiene lineas")
                errores.append(error)
                return errores

        else:
            errores.append("El movimiento ya está cerrado")
            return errores


class TraspasoBusiness(object):

    def __init__(self):
        self.tipo = "SAL"

    def crear_CabeceraTraspaso(self, formulario, usuario, clase):

        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            cabecera = MovimientoCabecera()
            cabecera.descripcion = datos_formulario.get('descripcion')
            cabecera.fecha = datos_formulario.get('fecha')
            cabecera.almacen_origen = datos_formulario.get(
                'almacen_origen'
            )
            cabecera.almacen_destino = datos_formulario.get(
                'almacen_destino'
            )
            cabecera.persona_entrega = datos_formulario.get('persona_entrega')
            cabecera.persona_recibe = datos_formulario.get('persona_recibe')
            cabecera.created_by = usuario
            cabecera.tipo = self.tipo
            cabecera.clasificacion = clase
            cabecera.save()

            return cabecera

    def actualizar_CabeceraTraspaso(self, cabecera, formulario, usuario):
        if cabecera.estado != "CER":
            if formulario.is_valid():
                cabecera = formulario.save(commit=False)
                cabecera.updated_by = usuario
                cabecera.save()

    def crear_CabeceraEntradaTraspaso(self, cabecera):

        entrada = MovimientoCabecera()

        entrada.descripcion = cabecera.descripcion
        entrada.fecha = cabecera.fecha
        entrada.almacen_origen = cabecera.almacen_origen
        entrada.almacen_destino = cabecera.almacen_destino
        entrada.persona_entrega = cabecera.persona_entrega
        entrada.persona_recibe = cabecera.persona_recibe
        entrada.created_by = cabecera.created_by
        entrada.tipo = "ENT"
        entrada.clasificacion = "TRA"
        entrada.estado = "TRAN"
        entrada.save()
        print entrada
        return entrada

    def crear_LineasDetalleEntradaTraspaso(self, salida, entrada):
        lineas = salida.movimientodetalle_set.all()
        for linea in lineas:
            mov_entrada = MovimientoDetalle()
            mov_entrada.cabecera = entrada
            mov_entrada.articulo = linea.articulo
            mov_entrada.cantidad = linea.cantidad
            mov_entrada.created_date = linea.created_date
            mov_entrada.updated_date = linea.updated_date
            mov_entrada.created_by = linea.created_by
            mov_entrada.updated_by = linea.updated_by
            mov_entrada.save()

        return True

    def guardar_LineasSalidaTraspasoEnStock(self, cabecera):

        # Se valida el estado de la cabecera:
        if cabecera.estado != "CER":

            lineas_detalle = cabecera.movimientodetalle_set.all()
            errores = []
            # Se valida que se tenga al menos una linea
            if len(lineas_detalle) > 0:

                # Recorriendo lineas
                for linea in lineas_detalle:

                    # Registro Existe
                    fila_stock = Stock.objects.filter(
                        almacen=cabecera.almacen_origen,
                        articulo=linea.articulo
                    )

                    if fila_stock:
                        if fila_stock[0].cantidad < linea.cantidad:
                            error = "%s %s %s %s" % (
                                "No hay articulos suficientes en almacen del articulo:",
                                fila_stock[0].articulo,
                                " Su cantidad actual es:",
                                fila_stock[0].cantidad
                            )
                            errores.append(error)
                            # return "No hay articulos suficientes en el stock."
                        else:
                            fila_stock[0].cantidad = fila_stock[
                                0].cantidad - linea.cantidad
                            fila_stock[0].save()

                    # Registro No Existe
                    else:
                        error = "%s: %s." % (
                            "No existe articulo registrado en stock ",
                            linea.articulo)
                        errores.append(error)
                        # return "No existe articulo registrado en el Stock"
                if len(errores) > 0:
                    return errores
                else:
                    cabecera.estado = "TRAN"
                    cabecera.save()
                    return True

            else:
                return "El detalle no tiene lineas"

        else:
            return "El movimiento ya está cerrado"

    def guardar_LineasEntradaTraspasoEnStock(self, cabecera):

        # Se valida el estado de la cabecera:
        if cabecera.estado != "CER":

            lineas_detalle = cabecera.movimientodetalle_set.all()

            # Se valida que se tenga al menos una linea
            if len(lineas_detalle) > 0:

                # Recorriendo lineas
                for linea in lineas_detalle:

                    # Registro Existe
                    fila_stock = Stock.objects.filter(
                        almacen=cabecera.almacen_destino,
                        articulo=linea.articulo
                    )

                    if fila_stock:

                        fila_stock[0].cantidad = fila_stock[
                            0].cantidad + linea.cantidad
                        fila_stock[0].save()

                    # Registro No Existe
                    else:

                        # Se crea el registro
                        Stock.objects.create(
                            almacen=cabecera.almacen_destino,
                            articulo=linea.articulo,
                            cantidad=linea.cantidad
                        )

                print "Se afecto el stock almacen destino"
                return "Exito"

            else:
                print "el detalle no tiene lineas"
                return "El detalle no tiene lineas"

        else:
            print "el movimiento ya esta cerrado"
            return "El movimiento ya está cerrado"

    def cerrar_Traspaso(self, entrada, usuario):

        if entrada.estado != "CER" and entrada.estado != "CAP":
            print "es diferente"
            # se busca el registro de salida
            salida = MovimientoCabecera.objects.filter(
                tipo="SAL",
                descripcion=entrada.descripcion,
                fecha=entrada.fecha,
                created_by=entrada.created_by)

            if salida:
                print salida
                salida[0].estado = "CER"
                salida[0].updated_by = usuario
                salida[0].save()

                entrada.estado = "CER"
                entrada.updated_by = usuario
                entrada.save()

                return True

            else:
                print "no hay salida"
                return False


class SalidaOrdenTrabajoBusiness(object):

    def crear_Cabecera(self, formulario, usuario):

        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            cabecera = MovimientoCabecera()
            cabecera.descripcion = datos_formulario.get('descripcion')
            cabecera.fecha = datos_formulario.get('fecha')
            cabecera.almacen_origen = datos_formulario.get(
                'almacen_origen'
            )
            cabecera.persona_entrega = datos_formulario.get(
                'persona_entrega'
            )
            cabecera.persona_recibe = datos_formulario.get(
                'persona_recibe'
            )
            cabecera.orden_trabajo = datos_formulario.get(
                'orden_trabajo'
            )
            cabecera.created_by = usuario
            cabecera.tipo = "SAL"
            cabecera.clasificacion = "OT"
            cabecera.save()

            # Buscar materiales en la orden, excepto herramientas
            materiales_ot = Material.objects.filter(
                orden__pk=cabecera.orden_trabajo.pk
            ).exclude(articulo__tipo="HER")

            # Crear lineas:
            for r in materiales_ot:
                linea = MovimientoDetalle()
                linea.cabecera = cabecera
                linea.cantidad = r.cantidad_estimada
                linea.articulo = r.articulo
                linea.created_by = usuario
                linea.save()

            return cabecera

    def actualizar_Cabecera(self, cabecera, formulario, usuario):

        # Si el estado de la orden es "CAPTURA"
        if cabecera.estado == "CAP":

            # Si formulario es valido:
            if formulario.is_valid():

                # Se guarda el nuevo valor de la orden
                orden_new = cabecera.orden_trabajo.pk

                cabecera = formulario.save(commit=False)
                cabecera.updated_by = usuario

                # Si la orden cambio en la cabecera:
                if cabecera.orden_trabajo.pk != orden_new:

                    # Eliminar Anteriores Lineas
                    lineas = MovimientoDetalle.objects.filter(cabecera=cabecera)
                    for r in lineas:
                        r.delete()

                    # Buscar materiales de la nueva orden, a excepcion de herramientas
                    materiales_ot = Material.objects.filter(
                        orden__pk=cabecera.orden_trabajo.pk
                    ).exclude(articulo__tipo="HER")

                    # Crear las nuevas lineas
                    for r in materiales_ot:
                        linea = MovimientoDetalle()
                        linea.cabecera = cabecera
                        linea.cantidad = r.cantidad_estimada
                        linea.articulo = r.articulo
                        linea.created_by = usuario
                        linea.save()

                cabecera.save()

    def guardar_Lineas(self, cabecera):

        # Genero lista de errores
        errores = []

        # Si el estado de la orden es "CAPTURA"
        if cabecera.estado == "CAP":

            # Se obtiene las lineas del movimiento
            lineas_detalle = cabecera.movimientodetalle_set.all()

            # Se valida que se tenga al menos una linea
            if len(lineas_detalle) > 0:

                # Se recorre las lineas a guardar
                for linea in lineas_detalle:

                    # Se consulta el stock por linea
                    fila_stock = Stock.objects.filter(
                        almacen=cabecera.almacen_origen,
                        articulo=linea.articulo
                    )

                    # Si se tiene el registro de stock:
                    if fila_stock:

                        # Si no hay suficiente stock
                        if fila_stock[0].cantidad < linea.cantidad:

                            msg_error = "No hay articulos suficientes en el stock, para %s (cantidad actual: %s)" % (
                                linea.articulo.descripcion, fila_stock[0].cantidad)
                            errores.append(msg_error)

                            return errores

                        # Si hay suficiente stock
                        else:

                            # Se busca la linea en material de la orden:
                            fila_material_orden = Material.objects.filter(
                                orden=cabecera.orden_trabajo,
                                articulo=linea.articulo
                            )

                            # Si encontro la linea:
                            if fila_material_orden:

                                # Actualiza la cantidad real de la orden
                                fila_material_orden[0].cantidad_real = \
                                    fila_material_orden[0].cantidad_real + linea.cantidad
                                fila_material_orden[0].save()

                            # Si no encontro la linea:
                            else:
                                msg_error = "No se puede proveer material que no está en la orden"
                                errores.append(msg_error)

                                return errores

                            # Se actualiza el stock:
                            fila_stock[0].cantidad = fila_stock[0].cantidad - linea.cantidad
                            fila_stock[0].save()

                    # Si no se tiene registro de stock
                    else:
                        msg_error = "No existe articulo registrado en el Stock"
                        errores.append(msg_error)
                        return errores

                # Se actualiza el estado de la cabecera:
                cabecera.estado = "CER"
                cabecera.save()

                return True

            else:
                msg_error = "El detalle no tiene lineas"
                errores.append(msg_error)

                return errores

        # Si el estado de la orden no es captura
        else:
            msg_error = "El movimiento ya está cerrado"
            errores.append(msg_error)

            return errores
