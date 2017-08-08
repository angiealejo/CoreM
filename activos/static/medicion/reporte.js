/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_medicion = window.location.origin + "/api/mediciones/"
var url_detalle = window.location.origin + "/equipos/"

// OBJS
var tabla = null
var modal = null
/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    tarjeta_filtros = new TarjetaFiltros()

})

/*-----------------------------------------------*\
            OBJETO: FILTROS
\*-----------------------------------------------*/

function TarjetaFiltros () {
    this.modal = new Modal()
    this.$equipo = $('#id_equipo')
    this.$odometro = $('#id_odometro')
    this.$tipo = $('#id_tipo')
    this.$fecha_inicio = $('#id_fecha_inicio')
    this.$fecha_fin = $('#id_fecha_fin')
    this.$boton_limpiar = $('#boton_limpiar')
    this.event_owner = null
    this.$celda_odometro = $('.odometro')
    this.$celda_equipo = $('.equipo')
    this.$equipos_lista = $('#equipos_lista')
    this.init()
}

TarjetaFiltros.prototype.init = function () {
    this.$equipo.select2(
        {   theme: "classic",
            allowClear:true,
    
        }
    )
    this.$odometro.select2(
        {   theme: "classic",
            allowClear:true,
    
        }
    )
    this.$fecha_inicio.datepicker(this.get_DateConfig())
    this.$fecha_fin.datepicker(this.get_DateConfig())
    this.$celda_odometro.on('click', this, this.click_Odometro)
    this.$boton_limpiar.on('click', this, this.click_BotonLimpiar)

}

TarjetaFiltros.prototype.get_DateConfig = function (){

    return {
        autoclose: true,
        language: 'es',
        todayHighlight: true,
        clearBtn: true,
        startDate: '2017-01-01',
        todayBtn: true,
    }
}
TarjetaFiltros.prototype.click_Odometro = function (e) {
    e.preventDefault()
    e.data.event_owner = $(this)
    id_odo = e.data.event_owner.attr('data-id-odo')
    id_equipo = e.data.event_owner.attr('data-id-eq')
    odometro = e.data.event_owner.attr('data-odometro')
    udm = e.data.event_owner.attr('data-udm')
    equipo = e.data.event_owner.attr('data-equipo')

    e.data.modal.set_ValoresData(id_odo, id_equipo, equipo, odometro, udm)
    e.data.modal.$id.modal('show')
}
TarjetaFiltros.prototype.click_BotonLimpiar = function (e) {
    e.preventDefault()
    e.data.$equipo.val("").trigger('change')
    e.data.$odometro.val("").trigger('change')
    e.data.$tipo.val("").trigger('change')
}

function Modal () {
    this.$id = $('#modal_nuevo')
    this.$equipo = $('#id_eq')
    this.$odometro = $('#id_odo')
    this.$udm = $('#id_udm')
    //Campo fecha
    this.$fecha = $('#id_fecha')
    this.$fecha_contenedor = $('#fecha_contenedor')
    this.$fecha_mensaje = $('#fecha_mensaje')
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
    this.$fecha.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha.datepicker(this.get_DateConfig());
    this.$fecha.datepicker('setDate', 'now');
    this.$hora.timepicker(
        {
            showInputs: false,
            minuteStep: 1
        }
    )
    fecha = new Date()
    hora = fecha.getHours()
    minutos = fecha.getMinutes()
    hora = this.get_FormatoUTC(hora, minutos)
    this.$hora.val(hora)
    this.$id.on('show.bs.modal', this, this.load)
    this.$boton_historial.on('click', this, this.click_BotonHistorial)
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

    // Se eliminan eventos viejos
    e.data.$boton_guardar.off("click")

    // Se limpian estilos
    e.data.clear_Estilos()

    // Se limpiar el formulario
    e.data.clear()  

    e.data.$boton_guardar.on(
        "click", 
        e.data, 
        e.data.nuevo
    )
    
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
Modal.prototype.validar = function () {

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
Modal.prototype.nuevo = function (e) {

    if (e.data.validar()) {

        hora = e.data.$hora.val().toLowerCase()
        hora =e.data.get_Hora(hora).trim()
        hora = "T"+hora+":00"

        $.ajax({
            url: url_medicion,
            method: "POST",
            data: {
                "equipo": e.data.$equipo.val(),
                "odometro": e.data.$odometro.val(),
                "fecha": e.data.$fecha.val() + hora,
                "lectura": e.data.$lectura.val(),
                "observaciones": e.data.$observaciones.val(),

            },
            success: function (response) {
                acumulado = tarjeta_filtros.event_owner.attr('data-acu')
                cifra = parseFloat(tarjeta_filtros.event_owner.text())
               
                if (acumulado=="SUM"){
                    lectura = e.data.$lectura.val()
                    console.log(typeof lectura)

                    suma = cifra + parseFloat(e.data.$lectura.val())
                    tarjeta_filtros.event_owner.text(suma)
                }
                if (acumulado=="ULT"){
                    
                    tarjeta_filtros.event_owner.text(e.data.$lectura.val())
                }
                alertify.success("Se guardó medición")
                e.data.$id.modal('hide')
                
            },
            error: function (response) {

                alertify.error("Ocurrio error al guardar")
            }
        })
        
    }
}
Modal.prototype.set_ValoresData = function(_idOdometro, _idEquipo, _Equipo, _Odometro, _Udm) {
    this.$equipo.val(_idEquipo)
    this.$odometro.val(_idOdometro)
    this.$udm.text("Equipo: "+ _Equipo+ ". Odómetro: " + _Odometro + ". UDM: " + _Udm)
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