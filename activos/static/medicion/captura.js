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
var url_grid = window.location.origin + "/api/mediciones/"


// OBJS
var tabla = null
var modal = null
/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {
    filtros = new Filtros()
    grid_mediciones = new GridMediciones()
    toolbar = new Toolbar()
    grid_resultados = new GridHistorico()
    filtros.llenar_SelectEquipos()

})

function FiltrosModal () {
    this.$fecha_inicio = $('#fecha_inicio')
    this.$fecha_fin = $('#fecha_fin')
    this.$boton_limpiar = $('#modal_btn_limpiar')
    this.$boton_buscar = $('#modal_btn_buscar')
    this.init()
}
FiltrosModal.prototype.init = function () {
    this.$fecha_inicio.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha_inicio.datepicker(this.get_DateConfig());
    this.$fecha_fin.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha_fin.datepicker(this.get_DateConfig());
    this.$boton_limpiar.on('click', this, this.click_BotonLimpiar)
    this.$boton_buscar.on('click', this, this.click_BotonBuscar)
}
FiltrosModal.prototype.get_DateConfig = function () {

    return {
        autoclose: true,
        language: 'es',
        todayHighlight: true,
        clearBtn: true,
        startDate: '2017-01-01',
        todayBtn: true
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
            OBJETO: FILTROS
\*-----------------------------------------------*/
function Filtros () {
    this.$tipo_equipo = $('#id_tipo_equipo')
    this.$equipo = $('#id_equipo')
    this.$equipo_texto = $('#equipo_texto')
    this.$equipo_id = $('#equipo_id')
    this.$fecha_inicio = $('#id_fecha_inicio')
    this.$fecha_fin = $('#id_fecha_fin')
    this.$tipo = $('#id_tipo')
    this.$boton_limpiar = $('#boton_limpiar')
    this.$boton_buscar = $('#boton_buscar')
    this.init()
}
Filtros.prototype.init = function () {
    this.$equipo.select2(

    )
    this.$fecha_inicio.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha_inicio.datepicker(this.get_DateConfig());
    this.$fecha_fin.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha_fin.datepicker(this.get_DateConfig());
    this.$boton_limpiar.on('click', this, this.click_BotonLimpiar)
    this.$tipo_equipo.on('change', this, this.change_TipoEquipo)
    this.$equipo.on('select2:select', this, this.select_Equipo)
}
Filtros.prototype.get_DateConfig = function () {

    return {
        autoclose: true,
        language: 'es',
        todayHighlight: true,
        clearBtn: true,
        startDate: '2017-01-01',
        todayBtn: true
    }
}
Filtros.prototype.click_BotonLimpiar = function (e) {
    e.preventDefault()
    e.data.$tipo.val(0).trigger('change')
    e.data.$fecha_inicio.val("")
    e.data.$fecha_fin.val("")
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
/*-----------------------------------------------*\
            OBJETO: GRID MEDICIONES
\*-----------------------------------------------*/
function GridMediciones () {
    this.modal = new Modal()
    this.modal_historico = new ModalHistorico()
    this.event_owner = null
    this.$fecha_exacta = null
    this.$odometro = null
    this.$celda_odometro = $('.odometro')
    this.$titulo_odometro = $('.titulo-odometro')
    this.$celda_equipo = $('.equipo')
    this.$equipos_lista = $('#equipos_lista')
    this.init()
}

GridMediciones.prototype.init = function () {
    
    this.$celda_odometro.on('click', this, this.click_Odometro)
    this.$celda_odometro.on('mouseover', this, this.OnCell)
    this.$celda_odometro.on('mouseout', this, this.OffCell)
    this.$titulo_odometro.on('mouseover', this, this.OnCell)
    this.$titulo_odometro.on('mouseout', this, this.OffCell)  

    this.$titulo_odometro.on('click', this, this.click_tituloOdometro)

}
GridMediciones.prototype.OnCell = function (e) {
    e.preventDefault()
    var event_owner = $(this)
    event_owner.addClass("corem-shadow")
}
GridMediciones.prototype.OffCell = function (e) {
    e.preventDefault()
    var event_owner = $(this)
    event_owner.removeClass("corem-shadow")
}
GridMediciones.prototype.get_DateConfig = function (){

    return {
        autoclose: true,
        language: 'es',
        todayHighlight: true,
        clearBtn: true,
        startDate: '2017-01-01',
        todayBtn: true,
    }
}
GridMediciones.prototype.click_Odometro = function (e) {
    e.preventDefault()
    e.data.event_owner = $(this)
    id_odo = e.data.event_owner.attr('data-id-odo')
    odometro_texto = e.data.event_owner.attr('data-odometro')
    odometro_udm = e.data.event_owner.attr ('data-udm')
    fecha = e.data.event_owner.attr('data-fecha')
    id_equipo = filtros.$equipo.val()
    e.data.modal.$fecha_texto.text("Fecha: " + fecha)
    e.data.modal.$odometro_texto.text("Odómetro: " + odometro_texto + ". UDM: " + odometro_udm)
    e.data.$odometro = id_odo
    e.data.$fecha_exacta = fecha
    e.data.modal.set_ValoresData(id_odo, id_equipo, fecha)
    e.data.modal.$id.modal('show')
}
GridMediciones.prototype.click_tituloOdometro = function (e) {
    e.preventDefault()
    e.data.event_owner = $(this)
    id_odometro = e.data.event_owner.attr('data-id')
    odometro_texto = e.data.event_owner.attr('data-odometro')
    console.log(odometro_texto)

    grid_mediciones.$odometro = id_odometro
    grid_mediciones.modal_historico.$odometro_texto.text("Odómetro: " + odometro_texto)

    e.data.modal_historico.load()
    e.data.modal_historico.$id.modal('show')

}
GridMediciones.prototype.get_Filtros = function (_page, _pageSize){
    console.log(this.$odometro)
    console.log(filtros.$equipo_id.val())
    return {
        page: _page,
        pageSize: _pageSize,
        equipo: filtros.$equipo_id.val(),
        odometro: this.$odometro,
        fecha_inicio: grid_mediciones.modal_historico.filtros.$fecha_inicio.val(), 
        fecha_fin: grid_mediciones.modal_historico.filtros.$fecha_fin.val()
        
    }
}
/*-----------------------------------------------*\
            OBJETO: MODAL
\*-----------------------------------------------*/
function Modal () {
    this.$id = $('#modal_nuevo')
    this.$equipo = $('#id_eq')
    this.$odometro = $('#id_odo')
    this.$udm = $('#id_udm')

    this.$odometro_texto = $('#odometro_texto')
    //Campo fecha
    this.$fecha_texto = $('#fecha_texto')

    //Campo hora
    this.$hora = $('#id_hora')
    this.$hora_contenedor = $('#hora_contenedor')
    this.$hora_mensaje = $('#hora_mensaje')
    //Campo lectura
    this.$lectura = $('#id_lectura')
    this.$lectura_contenedor = $('#lectura_contenedor')
    this.$lectura_mensaje = $('#lectura_mensaje')
    //Campo observaciones 
    this.$observaciones = $('#id_observaciones')
    this.$observaciones_contenedor = $('#observaciones_contenedor')
    this.$observaciones_mensaje = $('#observaciones_mensaje')

    this.$boton_historial= $('#boton_historial')
    this.$boton_guardar = $('#boton_guardar')

    this.init()
}
Modal.prototype.init = function () {

    this.$hora.timepicker(
        {
            showInputs: false,
            minuteStep: 60
        }
    )
    fecha = new Date()
    hora = fecha.getHours()
    minutos = fecha.getMinutes()
    // Formato con minutos diferentes
    //hora = this.get_FormatoUTC(hora, minutos)
    //this.$hora.val(hora)
    hora = this.get_HoraGeneral(hora)
    this.$fecha = null
    this.$hora.val(hora)
    this.$id.on('show.bs.modal', this, this.load)
    this.$boton_historial.on('click', this, this.click_BotonHistorial)
}
Modal.prototype.get_HoraGeneral = function(_horas) {
    horas = _horas
    minutos = '00'
    hora_utc = null
    if (hora == 12){
        hora_utc = hora + ":" + minutos + " PM"

    }
    else if (hora > 12 ) {
        hora_corta = hora - 12
        if (hora_corta<10){
            hora_corta.toString()
            
               nueva = "0" + hora_corta;
               hora_utc = nueva + ':' + minutos + ' PM' 
        }
        else {
            hora_utc = hora_corta + ':' + minutos + ' PM'
        }
    }
    else if (hora < 10){
        hora_utc = '0' + hora + ":" + minutos + ' AM'
    }
    else if (hora >= 10 && hora <=12 ){
        hora_utc = hora + ":" + minutos + ' AM'
    }
    return hora_utc

}
Modal.prototype.get_FormatoUTC = function (_horas, _minutos) {
    horas = _horas
    minutos = _minutos
    if (minutos==0){
        minutos = '00'
    }
    hora_utc = null
    if (hora == 12){
        hora_utc = hora + ":" + minutos + " PM"

    }
    else if (hora > 12 ) {
        hora_corta = hora - 12
        if (hora_corta<10){
            hora_corta.toString()
            
               nueva = "0" + hora_corta;
               hora_utc = nueva + ':' + minutos + ' PM' 
        }
        else {
            hora_utc = hora_corta + ':' + minutos + ' PM'
        }
    }
    else if (hora < 10){
        hora_utc = '0' + hora + ":" + minutos + ' AM'
    }
    else if (hora >= 10 && hora <=12 ){
        hora_utc = hora + ":" + minutos + ' AM'
    }
    return hora_utc
    
}
Modal.prototype.load = function (e) {

    //Se eliminan eventos viejos
    e.data.$boton_guardar.off("click")
    // //Se limpian estilos
    e.data.clear_Estilos()

    // // Se limpiar el formulario
    e.data.clear()  
    
    e.data.$boton_guardar.on(
        "click", 
        e.data, 
        e.data.nuevo
    )
    e.data.$id.on("keypress", e.data, e.data.guardar)
    e.data.$lectura.focus()
    
}
Modal.prototype.guardar = function (e) {
    
    if (e.which == 13) {

        grid_mediciones.modal.nuevo(e)
    }

}
Modal.prototype.click_BotonHistorial = function (e) {
    e.preventDefault()
    window.location.href = url_detalle + e.data.$equipo.val() + "/odometros/" + e.data.$odometro.val() + "/mediciones/"
}
Modal.prototype.get_Hora = function (_hora){
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
Modal.prototype.clear = function () {

    this.$lectura.val("")
    this.$observaciones.val("")
}
Modal.prototype.clear_Estilos = function () {
    
    this.$hora_contenedor.removeClass("has-error")  

    if(this.$hora_mensaje.hasClass('hidden') != null) { 
        this.$hora_mensaje.addClass('hidden')
    }
    this.$lectura_contenedor.removeClass("has-error")  

    if(this.$lectura_mensaje.hasClass('hidden') != null) { 
        this.$lectura_mensaje.addClass('hidden')
    } 
}
Modal.prototype.validar = function () {

    var bandera = true

    if ( this.$hora.val() == "") {
        this.$hora_contenedor.addClass("has-error")
        this.$hora_mensaje.removeClass("hidden")
        bandera = false
    }
    if ( this.$lectura.val() == "") {
        this.$lectura_contenedor.addClass("has-error")
        this.$lectura_mensaje.removeClass("hidden")
        bandera = false
    }

    return bandera
}
Modal.prototype.nuevo = function (e) {
    e.data.$id.off("keypress")
    if (e.data.validar()) {
        //fecha = 
        hora = e.data.$hora.val().toLowerCase()
        hora =e.data.get_Hora(hora).trim()
        hora = "T"+hora+":00"
        console.log("Equipo: " + e.data.$equipo.val())
        console.log("Odometro: "+ e.data.$odometro.val())
        console.log("Fecha:" + e.data.$fecha + hora)
        console.log("Lectura: " + e.data.$lectura.val())
        console.log("Observaciones:" + e.data.$observaciones.val())

        $.ajax({
            url: url_medicion,
            method: "POST",
            data: {
                "equipo": e.data.$equipo.val(),
                "odometro": e.data.$odometro.val(),
                "fecha": e.data.$fecha + hora,
                "lectura": e.data.$lectura.val(),
                "observaciones": e.data.$observaciones.val(),

            },
            success: function (response) {
                acumulado = grid_mediciones.event_owner.attr('data-acu')
                cifra = parseFloat(grid_mediciones.event_owner.text())
                grid_mediciones.event_owner.text(e.data.$lectura.val())
                
                // if (acumulado=="SUM"){
                //     lectura = e.data.$lectura.val()
                //     suma = cifra + parseFloat(e.data.$lectura.val())
                //     grid_mediciones.event_owner.text(suma)
                // }
                // if (acumulado=="ULT"){
                    
                //     grid_mediciones.event_owner.text(e.data.$lectura.val())
                // }
                alertify.success("Se guardó medición")
                e.data.$id.modal('hide')
                
            },
            error: function (response) {

                alertify.error("Ocurrio error al guardar")
            }
        })
        
    }
}
Modal.prototype.set_ValoresData = function(_idOdometro, _idEquipo, _fecha) {
    this.$equipo.val(_idEquipo)
    this.$odometro.val(_idOdometro)
    this.$fecha = fecha
    //this.$udm.text("Equipo: "+ _Equipo+ ". Odómetro: " + _Odometro + ". UDM: " + _Udm)
}
Modal.prototype.get_DateConfig = function () {

    return {
        autoclose: true,
        language: 'es',
        todayHighlight: true,
        clearBtn: true,
        startDate: '2017-01-01',
        todayBtn: true
    }
}
/*-----------------------------------------------*\
            OBJETO: MODAL FILTROS
\*-----------------------------------------------*/
/*-----------------------------------------------*\
            OBJETO: MODAL HISTORICO
\*-----------------------------------------------*/
function ModalHistorico () {
    this.filtros = new FiltrosModal()
    this.$id = $('#modal_historico')
    this.$contenido = $('#modal_contenido')
    this.$equipo = $('#id_eq')
    this.$odometro = $('#id_odo')
    this.$equipo_texto = $('#equipo_texto')
    this.$odometro_texto = $('#odo_texto')
    this.$fecha_texto = $('#fecha_texto')
    this.$udm = $('#id_udm')
    this.$usuario = $('#usuario')
    this.init()
}
ModalHistorico.prototype.init = function () {

    this.$contenido.addClass('corem-modal')
    this.filtros.$fecha_inicio.val(filtros.$fecha_inicio.val())
    this.filtros.$fecha_fin.val(filtros.$fecha_fin.val())
    //this.$id.on('hidden.bs.modal', this, this.actualizar_Pantalla)
}
ModalHistorico.prototype.actualizar_Pantalla = function (e) {
    console.log(grid_resultados.bandera)
    if (grid_resultados.bandera){
        location.reload()
    }
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
ModalHistorico.prototype.clear = function () {

    this.$lectura.val("")
    this.$observaciones.val("")
}
ModalHistorico.prototype.clear_Estilos = function () {
    
    this.$fecha_contenedor.removeClass("has-error")
    
    if(this.$fecha_mensaje.hasClass('hidden') != null) { 
        this.$fecha_mensaje.addClass('hidden')
    } 

    this.$hora_contenedor.removeClass("has-error")  

    if(this.$hora_mensaje.hasClass('hidden') != null) { 
        this.$hora_mensaje.addClass('hidden')
    }
    this.$lectura_contenedor.removeClass("has-error")  

    if(this.$lectura_mensaje.hasClass('hidden') != null) { 
        this.$lectura_mensaje.addClass('hidden')
    } 
}
ModalHistorico.prototype.validar = function () {

    var bandera = true

    if ( this.$fecha.val() == "") {
        this.$fecha_contenedor.addClass("has-error")
        this.$fecha_mensaje.removeClass("hidden")
        bandera = false
    }

    if ( this.$hora.val() == "") {
        this.$hora_contenedor.addClass("has-error")
        this.$hora_mensaje.removeClass("hidden")
        bandera = false
    }
    if ( this.$lectura.val() == "") {
        this.$lectura_contenedor.addClass("has-error")
        this.$lectura_mensaje.removeClass("hidden")
        bandera = false
    }

    return bandera
}
ModalHistorico.prototype.set_ValoresData = function(_idOdometro, _idEquipo, _Equipo, _Odometro, _Fecha) {

}
/*-----------------------------------------------*\
            OBJETO: GRID HISTORICO
\*-----------------------------------------------*/
function GridHistorico () {
    this.bandera = false
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
                var usuario = grid_mediciones.modal_historico.$usuario.val()

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
                var odometro = grid_mediciones.$odometro
                var lectura = e.model.lectura
                var usuario = grid_mediciones.modal_historico.$usuario.val()
                
                f = grid_mediciones.$fecha_exacta

                //console.log(f)
                var f = new Date(f);
                var timezoneoffset = -120
                fechita =  new Date( f.getTime() + Math.abs(f.getTimezoneOffset()*60000))
                
                //console.log(fechita)
                var hora = e.model.fecha
                var observaciones = e.model.observaciones
                
                nueva_fecha = new Date(
                    
                        Date.UTC(
                            fechita.getFullYear(),
                            fechita.getMonth(),
                            fechita.getDate(), 
                            hora.getHours(),
                            hora.getMinutes(),
                            hora.getSeconds()
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
            editor: this.timeEditor,
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
        // { command: 
        //     [
        //         {
        //             name:"edit",
        //             text:{
        //                     edit: "Editar",
        //                     update: "Actualizar", 
        //                     cancel: "Cancelar"
        //                 }
        //         }

        //     ],
        //     width: "180px"
        // },


    ]
}
GridHistorico.prototype.timeEditor = function (container, options) {
    $('<input data-text-field="' + options.field + '" data-value-field="' + options.field + '" data-bind="value:' + options.field + '" data-format="' + options.format + '"/>')
            .appendTo(container)
            .kendoTimePicker({});
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

                    return grid_mediciones.get_Filtros()
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

                url: url_grid,
                type: "GET",
                dataType: "json",
            },
            parameterMap: function (data, action) {
                if (action === "read") {

                    return grid_mediciones.get_Filtros(data.page, data.pageSize)
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

    var url_create = url_grid 
    
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

    var url_update = url_grid + _id  + "/"
    
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
GridHistorico.prototype.click_BotonEditar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_editar + fila.pk + "/"
}
GridHistorico.prototype.click_BotonMedicion = function (e) {
    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    var id_odometro = fila.pk
    window.location.href = url_medicion + id_odometro + '/mediciones/'

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
                        title: grid_mediciones.$fecha_exacta,
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: grid_mediciones.modal_historico.$equipo_texto.val() +  "_" + grid_mediciones.$fecha_exacta + ".xlsx"
            });
        });
}