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

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {
    filtros = new Filtros()
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
    this.$fecha_inicio.datetimepicker(this.get_DateConfig());
    this.$fecha_fin.datetimepicker(this.get_DateConfig());
    this.$boton_limpiar.on('click', this, this.click_BotonLimpiar)
    this.$tipo_equipo.on('change', this, this.change_TipoEquipo)
    this.$equipo.on('select2:select', this, this.select_Equipo)

}
Filtros.prototype.get_DateConfig = function () {
    return {
            locale: 'es',
            format: "YYYY-MM-DD HH:mm",
            minDate: "2017-01-01 00:00",
            stepping: 60,
            //defaultDate: new Date(),
            sideBySide: true,
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