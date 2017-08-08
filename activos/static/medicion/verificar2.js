/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/
//location.reload();
// URLS
var url_historico = window.location.origin + "/equipos/"
var url_medicion = window.location.origin + "/api/mediciones/"
var url_excel = window.location.origin + "/api/medicionexcel/"
var url_equipo = window.location.origin + "/api/equipoexcel/"
var url_detalle = window.location.origin + "/equipos/"
var url_historial = window.location.origin + "/mediciones/historial/equipo/"


// OBJS
var tabla = null
var modal = null
var grid_resultados = null
/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {
    filtros = new Filtros()
    tabla = new Tabla()
    grid_resultados = new GridHistorico()
    filtros.llenar_SelectEquipos()

})

/*-----------------------------------------------*\
            OBJETO: FILTROS
\*-----------------------------------------------*/
function Filtros () {
    this.$tipo_equipo = $('#id_tipo_equipo')
    this.$equipo = $('#id_equipo')
    this.$equipo_texto = $('#equipo_texto')
    this.$equipo_id = $('#equipo_id')
    this.$tipo = $('#id_tipo')
    this.$boton_limpiar = $('#boton_limpiar')
    this.$boton_buscar = $('#boton_buscar')
    this.$boton_historial = $('#boton_historial')

    this.horometro = null
    this.init()
}
Filtros.prototype.init = function () {
    this.$equipo.select2()
    this.$boton_limpiar.on('click', this, this.click_BotonLimpiar)
    this.$boton_historial.on('click', this, this.click_BotonHistorial)
    this.$tipo_equipo.on('change', this, this.change_TipoEquipo)
    this.$equipo.on('select2:select', this, this.select_Equipo)
}
Filtros.prototype.click_BotonHistorial = function (e) {
    e.preventDefault()
    window.open(url_historial  + e.data.$equipo.val() + "/tipo_odometro/" + e.data.$tipo.val() + "/", '_blank')
}
Filtros.prototype.click_BotonLimpiar = function (e) {
    e.preventDefault()
    e.data.$tipo.val(0).trigger('change')
}
Filtros.prototype.select_Equipo = function (e) {
    if (e.data.$equipo.val() != 0){
        e.data.$boton_buscar.prop('disabled', false)
    }
    else if (e.data.$equipo.val() == 0){
        e.data.$boton_buscar.prop('disabled', true)
    }
    
}
Filtros.prototype.llenar_SelectEquipos = function () {
    filtros.$equipo.find('option').remove().end().append($('<option>').attr('value', 0).text("Seleccione..."))

    $.ajax({
            url: url_equipo,
            method: "GET",
            data: {
                "tipo": filtros.$tipo_equipo.val()
            },
            success: function (response) {
            $.each(response, function(index, item) 
                {   
                    filtros.$equipo.append($('<option>').attr('value',item.pk).text("("+item.tag+") "+item.descripcion))
                    filtros.$equipo.trigger('change')
                }
            )
            filtros.$equipo.val(filtros.$equipo_id.val())
            filtros.$equipo.trigger('change')
                
            },
            error: function () {

                alertify.error("Ocurrió un error al consultar los equipos")
            }
    })
}
Filtros.prototype.change_TipoEquipo = function (e) {
    e.preventDefault()
    var event_owner = $(this)
    filtros.$equipo.find('option').remove().end().append($('<option>').attr('value', 0).text("Seleccione..."))

    $.ajax({
            url: url_equipo,
            method: "GET",
            data: {
                "tipo": event_owner.val()
            },
            success: function (response) {
            $.each(response, function(index, item) 
                {   
                    filtros.$equipo.append($('<option>').attr('value',item.pk).text("("+item.tag+") "+item.descripcion))
                    filtros.$equipo.trigger('change')
                }
            )
                
            },
            error: function () {

                alertify.error("Ocurrió un error al consultar los equipos")
            }
    })
}

function Tabla () {
    this.modal_historico = new ModalHistorico()
    this.modal_observacion = new ModalObservacion ()
    this.event_owner = null
    this.$usuario = $('#id_profile')
    this.$celda_odometro = $('.odometro')
    this.$fecha_general = $('#fecha')
    this.$fecha = $('.date-input')
    this.$fila = $('.fila-odometro')
    this.$celda_lectura = $('.lectura')
    this.$celda_fecha_nueva = $('.fecha-lectura')
    this.$celda_lectura_texto = $("input[data-tipo='texto']")
    this.$celda_lectura_opcional = $("select[data-tipo='opcional']")
    this.$boton_observacion = $("a[data-observacion='observacion']")
    this.$total_horas = null
    this.odometro = null
    this.init()
}
Tabla.prototype.init = function () {
    this.$fecha_general.datetimepicker(this.get_DateConfig())
    this.$fecha.datetimepicker(this.get_DateConfig())
    this.$celda_odometro.on('mouseover', this, this.OnCell)
    this.$celda_odometro.on('mouseout', this, this.OffCell)
    this.$celda_lectura.on('keypress', this, this.validar_Entrada)
    this.$celda_lectura_texto.on('keypress', this, this.validar_EntradaTexto)
    this.$celda_lectura_texto.on('focus', this, this.mostrar_TipoCampo)
    this.$celda_lectura_texto.on('blur', this, this.ocultar_TipoCampo)
    this.$celda_lectura_opcional.on('keypress', this, this.validar_EntradaOpcion)
    this.$celda_fecha_nueva.on('keydown', this, this.validar_Entrada)
    this.$fecha_general.on('dp.change', this, this.actualizar_Datepickers)
    this.$celda_odometro.on('click', this, this.click_tituloOdometro)
    this.$boton_observacion.on('click', this.click_BotonObservacion)
}
Tabla.prototype.click_BotonObservacion = function (e) {
    event_owner = $(this)
    id_medicion = event_owner.parents('tr').find("input[data-medicion='medicion']").val()
    tabla.modal_observacion.$id.modal('show')
    tabla.modal_observacion.$id_medicion.val(id_medicion)

}
Tabla.prototype.mostrar_TipoCampo = function (e) {

    var event_owner = $(this)

    event_owner.parents("tr").find('.lectura-contenedor').addClass('has-warning')
    event_owner.parents("tr").find('.campo-msj').removeClass("hidden")
}
Tabla.prototype.ocultar_TipoCampo = function (e) {
    var event_owner = $(this)

    event_owner.parents("tr").find('.lectura-contenedor').removeClass('has-warning')
    event_owner.parents("tr").find('.campo-msj').addClass("hidden")
}
Tabla.prototype.validarCampos = function (_event_owner) {

    var bandera = true
    if (_event_owner.parents("tr").find('.fecha-lectura').val() == '') {
        _event_owner.parents("tr").find('.fecha-contenedor').addClass('has-error')
        _event_owner.parents("tr").find('.fecha-msj').removeClass("hidden")
        bandera = false
    }
    if (_event_owner.parents("tr").find('.lectura').val() == '' || _event_owner.parents("tr").find('.lectura').val() == '0') {
        _event_owner.parents("tr").find('.lectura-contenedor').addClass('has-error')
        _event_owner.parents("tr").find('.lectura-msj').removeClass("hidden")
        bandera = false
    }
    return bandera

}
Tabla.prototype.validarCamposTexto = function(_event_owner) {
    var bandera = true
    if (_event_owner.parents("tr").find('.fecha-lectura').val() == '') {
        _event_owner.parents("tr").find('.fecha-contenedor').addClass('has-error')
        _event_owner.parents("tr").find('.fecha-msj').removeClass("hidden")
        bandera = false
    }
    if (_event_owner.parents("tr").find("input[data-tipo='texto']").val() == '' || _event_owner.parents("tr").find('.lectura').val() == '0') {
        _event_owner.parents("tr").find('.lectura-contenedor').addClass('has-error')
        _event_owner.parents("tr").find('.lectura-msj').removeClass("hidden")
        bandera = false
    }
    return bandera
}
Tabla.prototype.validarCamposOpcion = function (_event_owner) {
    var bandera = true
    if (_event_owner.parents("tr").find('.fecha-lectura').val() == '') {
        _event_owner.parents("tr").find('.fecha-contenedor').addClass('has-error')
        _event_owner.parents("tr").find('.fecha-msj').removeClass("hidden")
        bandera = false
    }
    if (_event_owner.parents("tr").find("select[data-tipo='opcional']").val() == '' || _event_owner.parents("tr").find('.lectura').val() == '0') {
        _event_owner.parents("tr").find('.lectura-contenedor').addClass('has-error')
        _event_owner.parents("tr").find('.lectura-msj').removeClass("hidden")
        bandera = false
    }
    return bandera
}
Tabla.prototype.validar_Entrada = function (e) {

    if (e.which == 13) {
        e.preventDefault()
        var event_owner = $(this)
        if (e.data.validarCampos(event_owner)){
            var odometro = event_owner.parents("tr").find('.odometro-id').val()
            var equipo = event_owner.parents("tr").find('.equipo-id').val()
            var fecha = event_owner.parents("tr").find('.fecha-lectura').val()
            var lectura = event_owner.parents("tr").find('.lectura').val()
            fecha_formateada = e.data.formatear_Fecha(fecha)
            nueva_fecha = fecha_formateada[0]+"T"+fecha_formateada[1]+":00"
            e.data.guardar_Medicion(event_owner, odometro, equipo, nueva_fecha, lectura, null)  
        }   
    }
}
Tabla.prototype.validar_EntradaTexto = function (e) {
    if (e.which == 13) {
        e.preventDefault()
        var event_owner = $(this)
        if (e.data.validarCamposTexto(event_owner)){
            var odometro = event_owner.parents("tr").find('.odometro-id').val()
            var equipo = event_owner.parents("tr").find('.equipo-id').val()
            var fecha = event_owner.parents("tr").find('.fecha-lectura').val()
            var lectura = event_owner.parents("tr").find("input[data-tipo='texto']").val()
            fecha_formateada = e.data.formatear_Fecha(fecha)
            nueva_fecha = fecha_formateada[0]+"T"+fecha_formateada[1]+":00"
            e.data.guardar_Medicion(event_owner, odometro, equipo, nueva_fecha, 0, lectura)  
        }
    }
} 
Tabla.prototype.validar_EntradaOpcion = function (e) {
    if (e.which == 13) {
        e.preventDefault()
        var event_owner = $(this)
        if (e.data.validarCamposOpcion(event_owner)){
            var odometro = event_owner.parents("tr").find('.odometro-id').val()
            var equipo = event_owner.parents("tr").find('.equipo-id').val()
            var fecha = event_owner.parents("tr").find('.fecha-lectura').val()
            var lectura = event_owner.parents("tr").find("select[data-tipo='opcional']").val()
            fecha_formateada = e.data.formatear_Fecha(fecha)
            nueva_fecha = fecha_formateada[0]+"T"+fecha_formateada[1]+":00"
            e.data.guardar_Medicion(event_owner, odometro, equipo, nueva_fecha, 0, lectura)  
        }
    }

}
Tabla.prototype.get_DateConfig = function () {
    return {
            locale: 'es',
            format: "YYYY-MM-DD HH:mm",
            minDate: "2017-01-01 00:00",
            stepping: 60,
            defaultDate: new Date(),
            sideBySide: true,
        }
}
Tabla.prototype.OnCell = function (e) {
    e.preventDefault()
    var event_owner = $(this)
    event_owner.addClass("corem-shadow")
}
Tabla.prototype.OffCell = function (e) {
    e.preventDefault()
    var event_owner = $(this)
    event_owner.removeClass("corem-shadow")
}
Tabla.prototype.clear_Estilos = function (_event_owner) {

    _event_owner.parents("tr").find('.fecha-contenedor').removeClass('has-error')
   if(_event_owner.parents("tr").find('.fecha-msj').hasClass('hidden') != null){
        _event_owner.parents("tr").find('.fecha-msj').addClass('hidden')
   } 

   _event_owner.parents("tr").find('.lectura-contenedor').removeClass('has-error')

   if(_event_owner.parents("tr").find('.lectura-msj').hasClass('hidden') != null){
        _event_owner.parents("tr").find('.lectura-msj').addClass('hidden')
   }
  
}
Tabla.prototype.guardar_Medicion = function (_event_owner, _odometro, _equipo, _fecha, _lectura, _observaciones) {
    /* TODO: 
       Comparar la fecha del grid con la fecha ingresada para decidir que info mostrar en la celda
    */
    $.ajax({
            url: url_medicion,
            method: "POST",
            data: {
                "equipo": _equipo,
                "odometro": _odometro,
                "fecha": _fecha,
                "lectura": _lectura,
                "observaciones": _observaciones,
                "created_by": this.$usuario.val()
            },
            success: function (response) {
        
                _event_owner.parents("tr").find('.lectura').val("")
                fecha_nueva = new Date(_fecha)
                moment.locale('es')
                fecha_formateada = moment(fecha_nueva).format("DD/MM/YYYY HH:mm")
                _event_owner.parents("tr").find('.ultima-fecha').text(fecha_formateada)
                if (_event_owner.context.localName == 'select' || _event_owner.context.type == 'text'){
                    _event_owner.parents("tr").find('.ultima-lectura').text(_observaciones)
                }
                else {
                    _event_owner.parents("tr").find('.ultima-lectura').text(_lectura)
                }
                _event_owner.parents("tr").find("input[data-medicion='medicion']").val(response.pk)
                tabla.clear_Estilos(_event_owner)
                alertify.success("Se guardó medición")
                var index = $("[data-lectura='lectura']").index(_event_owner) + 1
                $("[data-lectura='lectura']").eq(index).focus()
            },
            error: function (response) {

                alertify.error("Ocurrio error al guardar")
            }
        })
}
Tabla.prototype.formatear_Fecha = function (_fecha) {
    formato = _fecha.split(' ')
    return formato
}
Tabla.prototype.actualizar_Datepickers = function (e) {
    fecha = moment(e.date._d).format('YYYY-MM-DD HH:mm');
    e.data.$fecha.datetimepicker('date', fecha)
}
Tabla.prototype.click_tituloOdometro = function (e) {
    e.preventDefault()
    e.data.event_owner = $(this)
    id_odometro = e.data.event_owner.attr('data-id-odo')
    odometro_texto = e.data.event_owner.attr('data-odometro')
    tabla.modal_historico.$odometro_texto.text("Odómetro: " + odometro_texto)
    tabla.modal_historico.odometro = id_odometro
    e.data.modal_historico.load()
    e.data.modal_historico.$id.modal('show')
   
}
Tabla.prototype.get_Filtros = function (_page, _pageSize){

    return {
        page: _page,
        pageSize: _pageSize,
        equipo: filtros.$equipo_id.val(),
        odometro: tabla.modal_historico.odometro,
        fecha_inicio: this.modal_historico.filtros.$fecha_inicio.val(),
        fecha_fin: this.modal_historico.filtros.$fecha_fin.val()
    }
}
/*-----------------------------------------------*\
            OBJETO: MODAL OBSERVACION
\*-----------------------------------------------*/
function ModalObservacion () {
    this.$id = $('#win_observacion')
    this.$id_medicion = $('#medicion_id')
    this.$observaciones_contenedor = $('#observaciones_contenedor')
    this.$observaciones_mensaje = $('.observacion-msj')
    this.$observaciones = $('#observaciones')
    this.$boton_guardar = $('#btn_obs-save')
    this.init()
}
ModalObservacion.prototype.init = function () {
    // Se asoscia eventos al abrir el modal
    this.$id.on('show.bs.modal', this, this.load)
}
ModalObservacion.prototype.load = function (e) {

    var event_owner = $(e.relatedTarget)

    // Se eliminan eventos viejos
    e.data.$boton_guardar.off("click")

    // Se limpian estilos
    e.data.clear_Estilos()

    // Se limpiar el formulario
    e.data.clear()  

    // Se asoscia el evento que se utilizara para guardar
    e.data.$boton_guardar.on(
        "click", 
        e.data, 
        e.data.nuevo
    )
}
ModalObservacion.prototype.clear = function () {

    this.$observaciones.val("")
}
ModalObservacion.prototype.clear_Estilos = function () {
    
    this.$observaciones_contenedor.removeClass("has-error")
    
    if(this.$observaciones_mensaje.hasClass('hidden') != null) { 
        this.$observaciones_mensaje.addClass('hidden')
    } 
}
ModalObservacion.prototype.validar = function () {

    var bandera = true

    if ( this.$observaciones.val() == "") {
        this.$observaciones_contenedor.addClass("has-error")
        this.$observaciones_mensaje.removeClass("hidden")
        bandera = false
    }

    return bandera
}
ModalObservacion.prototype.nuevo = function (e) {

    if (e.data.validar()) {

        $.ajax({
            url: url_medicion + e.data.$id_medicion.val() + "/",
            method: "PATCH",
            data: {
                "observaciones" : e.data.$observaciones.val()
            },
            success: function (response) {

                e.data.$id.modal('hide')
                alertify.success("Observacion guardada")
            },
            error: function (response) {

                alertify.error("Ocurrio error al agregar observaciones")
            }
        })
        
    }
}
/*-----------------------------------------------*\
            OBJETO: MODAL HISTORICO
\*-----------------------------------------------*/
function ModalHistorico () {
    this.filtros = new FiltrosModal()
    this.toolbar = new Toolbar()
    this.$id = $('#modal_historico')
    this.$contenido = $('#modal_contenido')
    this.$equipo = $('#equipo')
    this.odometro = null
    this.$equipo_texto = $('#equipo_texto')
    this.$odometro_texto = $('#odo_texto')
    this.$usuario = null
    this.init()
}
ModalHistorico.prototype.init = function () {

    this.$contenido.addClass('corem-modal')
    this.$id.on('show.bs.modal', this, this.load)

}
ModalHistorico.prototype.load = function () {
    grid_resultados.kfuente_datos.page(1)
    grid_resultados.kfuente_datos.read()
    grid_resultados.kfuente_datos_excel.read()
}
ModalHistorico.prototype.get_Hora = function (_hora){
    this.hora = _hora
    var horas = parseInt(this.hora.substr(0, 2))

    if(this.hora.indexOf('am') != -1) {
        this.hora = this.hora.replace('12', '0')
        
    }
    if(this.hora.indexOf('pm')  != -1) {
        if(horas<10){
            
            this.hora = this.hora.replace(horas, (horas + 12))
            this.hora = this.hora.substr(1, 5)

        }
        else if(horas==12){

            this.hora = this.hora
        }
        else{

            this.hora = this.hora.replace(horas, (horas + 12)) 
        }
           
    }
        this.hora = this.hora.replace(/(am|pm)/, '')
        return this.hora
        
}
/*-----------------------------------------------*\
            OBJETO: FILTROS
\*-----------------------------------------------*/
function FiltrosModal () {
    this.$fecha_inicio = $('#fecha_inicio')
    this.$fecha_fin = $('#fecha_fin')
    this.$boton_limpiar = $('#modal_btn_limpiar')
    this.$boton_buscar = $('#modal_btn_buscar')
    this.init()
}
FiltrosModal.prototype.init = function () {
    this.$fecha_inicio.datetimepicker(this.get_DateConfig())
    this.$fecha_fin.datetimepicker(this.get_DateConfig())
    this.$boton_limpiar.on('click', this, this.click_BotonLimpiar)
    this.$boton_buscar.on('click', this, this.click_BotonBuscar)
}
FiltrosModal.prototype.get_DateConfig = function () {
    return {
            locale: 'es',
            format: "YYYY-MM-DD",
            minDate: "2017-01-01",
            defaultDate: new Date(),
        }
}
FiltrosModal.prototype.click_BotonLimpiar = function (e) {
    e.preventDefault()
    e.data.$fecha_inicio.val("")
    e.data.$fecha_fin.val("")
}
FiltrosModal.prototype.click_BotonBuscar = function (e) {
    e.preventDefault()
    grid_resultados.buscar()
}
/*-----------------------------------------------*\
            OBJETO: GRID HISTORICO
\*-----------------------------------------------*/
function GridHistorico () {

    this.$id = $('#grid_principal')
    this.kfuente_datos = null
    this.kfuente_datos_excel = null
    this.kgrid = null

    this.init()
}
GridHistorico.prototype.init = function () {

    kendo.culture("es-MX")

    this.kfuente_datos = new kendo.data.DataSource(this.get_FuenteDatosConfig())
    this.kfuente_datos_excel = new kendo.data.DataSource(this.get_FuenteDatosExcel())

    this.kGrid = this.$id.kendoGrid(this.get_Config())
}
GridHistorico.prototype.get_Config = function () {

    return {
        dataSource: this.kfuente_datos,
        columnMenu: false,
        groupable: false,
        sortable: false,
        editable: "inline",
        resizable: true,
        selectable: true,
        scrollable: false,
        columns: this.get_Columnas(),
        scrollable: true,
        pageable: true,

        save: function(e) {
            
            e.preventDefault()
            if (e.model.equipo){
                var pk = e.model.pk
                var equipo = e.model.equipo
                var odometro = e.model.odometro
                var lectura = e.model.lectura
                var fecha = e.model.fecha
                var observaciones = e.model.observaciones
                var usuario = tabla.$usuario.val()

                nueva_fecha = new Date(
                    Date.UTC(
                        fecha.getFullYear(),
                        fecha.getMonth(),
                        fecha.getDate(), 
                        fecha.getHours(),
                        fecha.getMinutes(),
                        fecha.getSeconds()
                        )
                    )

                grid_resultados.actualizar_Medicion(pk, equipo, odometro, lectura, nueva_fecha, observaciones, usuario)
                grid_resultados.kfuente_datos.read()
                grid_resultados.kfuente_datos_excel.read()
                
            }
            else {
                var equipo = filtros.$equipo_id.val()
                var odometro = tabla.modal_historico.odometro
                var lectura = e.model.lectura
                var fecha = e.model.fecha
                var observaciones = e.model.observaciones
                var usuario = tabla.$usuario.val()
                
                nueva_fecha = new Date(
                    Date.UTC(
                        fecha.getFullYear(),
                        fecha.getMonth(),
                        fecha.getDate(), 
                        fecha.getHours(),
                        fecha.getMinutes(),
                        fecha.getSeconds()
                        )
                    )
                
                grid_resultados.registrar_Medicion(equipo, odometro, lectura, nueva_fecha, observaciones, usuario)
                grid_resultados.kfuente_datos.read()
                grid_resultados.kfuente_datos_excel.read()
               
            }
        },
        cancel: function (e) {
            e.preventDefault()
            grid_resultados.kfuente_datos.read()
        }
           
    }     
}
GridHistorico.prototype.get_Campos = function (e) {

    return {
        fecha: { type: "date" },
        lectura: { type: "string" },
        lectura: { type: "observaciones" },
        
    }
}
GridHistorico.prototype.get_Columnas = function (e) {

    return [
        { field: "fecha" ,
            title: "Fecha",
            width: "120px",
            format:"{0:dd-MMMM-yyyy HH:mm}",
            validation: { required: true } },
        { field: "lectura" ,
          title: "Lectura",
          width: "120px",
          type: "number",
          validation: { min: 0, required: true },
          editor: this.editNumberWithoutSpinners,
          editable: true
        },
        { field: "observaciones", title: "Observaciones", width:"120px" },
        { field: "creado_por", title: "Creado por", width:"120px", IsNotEditable: true },
        { field: "modificado_por", title: "Modificado por", width:"120px", IsNotEditable: true },
        { command: 
            [
                {
                    name:"edit",
                    text:{
                            edit: "Editar",
                            update: "Actualizar", 
                            cancel: "Cancelar"
                        }
                }

            ],
            width: "180px"
        },
    ]
}
GridHistorico.prototype.editNumberWithoutSpinners = function (container, options) {
    $('<input data-text-field="' + options.field + '" ' +
            'data-value-field="' + options.field + '" ' +
            'data-bind="value:' + options.field + '" ' +
            'data-format="' + options.format + '"/>')
            .appendTo(container)
            .kendoNumericTextBox({
                spinners : false
            });
}
GridHistorico.prototype.get_FuenteDatosExcel = function (e) {

    return {

        transport: {
            read: {

                url: url_excel,
                type: "GET",
                dataType: "json",
            },
            parameterMap: function (data, action) {
                if (action === "read") {

                    return tabla.get_Filtros()
                }
            }
        },
        schema: {
            model: {
                fields: this.get_Campos()
            }
        },
        error: function (e) {
            alertify.error("Status: " + e.status + "; Error message: " + e.errorThrown)
        },
    }
    
}
GridHistorico.prototype.get_FuenteDatosConfig = function (e) {

    return {

        serverPaging: true,
        pageSize: 10,
        transport: {
            read: {

                url: url_medicion,
                type: "GET",
                dataType: "json",
            },
            parameterMap: function (data, action) {
                if (action === "read") {

                    return tabla.get_Filtros(data.page, data.pageSize)
                }
            }
        },
        schema: {
            data: "results",
            total: "count",
            model: {
                fields: this.get_Campos()
            }
        },
        
        error: function (e) {
            alertify.error("Status: " + e.status + "; Error message: " + e.errorThrown)
        },
    }
}
GridHistorico.prototype.registrar_Medicion = function (_equipo, _odometro, _lectura, _fecha, _observaciones, _usuario) {

    var url_create = url_medicion 
    
    data = {
        'equipo': _equipo,
        'odometro': _odometro, 
        'lectura': _lectura,
        'fecha': _fecha,
        'observaciones': _observaciones,
        'created_by': _usuario,
    }

    $.ajax({

        url: url_create,
        data : JSON.stringify(data),
        dataType: "json",
        type: "POST",
        contentType: "application/json; charset=utf-8",

        success: function (e) {
            alertify.warning("Se guardó el registro")
        },
        error: function (e) {
            alertify.error("No se pudo guardar el registro")
        }
    })    

}
GridHistorico.prototype.actualizar_Medicion = function (_id, _equipo, _odometro, _lectura, _fecha, _observaciones, _usuario) {

    var url_update = url_medicion + _id  + "/"
    
    data = {
        'equipo': _equipo,
        'odometro': _odometro, 
        'lectura': _lectura,
        'fecha': _fecha,
        'observaciones': _observaciones,
        'updated_by': _usuario,
    }

    $.ajax({

        url: url_update,
        data : JSON.stringify(data),
        dataType: "json",
        type: "PUT",
        contentType: "application/json; charset=utf-8",

        success: function (e) {
            alertify.warning("Se guardó el registro")
        },
        error: function (e) {
            alertify.error("No se pudo guardar el registro")
        }
    })    

}
GridHistorico.prototype.buscar =  function() {
    this.kfuente_datos.page(1)
    this.kfuente_datos_excel.read()
}
/*-----------------------------------------------*\
            OBJETO: TOOLBAR
\*-----------------------------------------------*/

function Toolbar() {

    this.$boton_nuevo = $("#boton_nuevo")
    this.$boton_exportar = $("#boton_exportar")

    this.init()
}
Toolbar.prototype.init = function (e) {

    this.$boton_nuevo.on("click", this, this.click_BotonNuevo)
    this.$boton_exportar.on("click", this, this.click_BotonExportar)
}
Toolbar.prototype.click_BotonNuevo = function (e) {

    e.preventDefault()
    grid_resultados.$id.data("kendoGrid").addRow();
}
Toolbar.prototype.Inicializar_CeldasExcel = function (e) {

    if (grid_resultados.get_Columnas != null)
    {
        if (grid_resultados.get_Columnas.length != 1) {
            grid_resultados.get_Columnas.length = 0;
        }
    }

    this.kRows = [{
        cells: [
            { value: 'Fecha'},
            { value: 'Lectura' },
            { value: 'Observaciones' },
            { value: 'Creado por' },
            { value: 'Modificado por' },
        ]
    }];
}
Toolbar.prototype.click_BotonExportar = function (e) {

    e.preventDefault();
    e.data.Inicializar_CeldasExcel();

    
        grid_resultados.kfuente_datos_excel.fetch(function () {

            var data = this.data();
            for (var i = 0; i < data.length; i++) {

                e.data.kRows.push({
                    cells: [
                        { value: data[i].fecha, format: "dd/MM/yyyy hh:mm" },
                        { value: data[i].lectura },
                        { value: data[i].observaciones },
                        { value: data[i].creado_por },
                        { value: data[i].modificado_por },
                    ]
                })
            }
            var workbook = new kendo.ooxml.Workbook({
                sheets: [
                    {
                        columns: [
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                        ],
                        title: tabla.modal_historico.filtros.$fecha_inicio.val() + "-" + tabla.modal_historico.filtros.$fecha_fin.val(),
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: tabla.modal_historico.$equipo_texto.text() +".xlsx"
            });
        });
}

