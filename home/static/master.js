/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_mensajes_m = window.location.origin + "/api/mensajes/"
var url_mensaje_m  = window.location.origin + "/mensajes/revisar/mensaje_id/"


var pagina = null
var view_mensajes = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

	pagina = new Pagina()
	view_mensajes = new VisorMensajes()
})

// Spinner en Ajax
$(document).ajaxStart(function() { Pace.restart() })

/*-----------------------------------------------*\
            OBJETO: PAGINA
\*-----------------------------------------------*/

function Pagina() {

	this.$titulo = $('#titulo')

	this.set_PageActive()
	this.init_Alertify()
}
Pagina.prototype.set_PageActive = function () {

	// Se marca la pagina activa en el menu
	if ( this.$titulo.text() == "Inicio") {
		
		this.activar_Opcion("opt_dashboard")
	}
	else if ( this.$titulo.text() == "Equipos") {

		this.activar_Arbol("tree_activos")
		this.activar_Opcion("opt_equipos")
	}
	else if ( this.$titulo.text() == "Ubicaciones") {
		
		this.activar_Arbol("tree_activos")
		this.abrir_Submenu("tree_act_conf")
		this.activar_Opcion("opt_ubicaciones")
	}
	else if ( this.$titulo.text() == "Unidad de Medida de Odometro") {
		
		this.activar_Arbol("tree_activos")
		this.abrir_Submenu("tree_act_conf")
		this.activar_Opcion("opt_odometros_udm")
	}			
	else if ( this.$titulo.text() == "Tipos de Odómetros") {
		
		this.activar_Arbol("tree_activos")
		this.abrir_Submenu("tree_act_conf")
		this.activar_Opcion("opt_odometros_tipo")
	}
	else if ( this.$titulo.text() == "Odómetros") {
		
		this.activar_Arbol("tree_activos")
		this.activar_Opcion("opt_odometros")
	}	
	else if ( this.$titulo.text() == "Resumen") {
		
		this.activar_Arbol("tree_activos")
		this.abrir_Submenu("tree_act_mediciones")
		this.activar_Opcion("opt_mediciones")
		this.activar_Opcion("opt_mediciones_resumen")
	}
	else if ( this.$titulo.text() == "Captura" || this.$titulo.text() == "Historial" || this.$titulo.text() == "Log") {
		
		this.activar_Arbol("tree_activos")
		this.abrir_Submenu("tree_act_mediciones")
		this.activar_Opcion("opt_mediciones")
		this.activar_Opcion("opt_mediciones_captura")
	}
	else if ( this.$titulo.text() == "Reportes") {
		
		this.activar_Arbol("tree_activos")
		this.activar_Opcion("opt_reportes")
	}
	else if ( this.$titulo.text() == "Almacenes") {

		this.activar_Arbol("tree_inventarios")
		this.abrir_Submenu("tree_inv_conf")
		this.activar_Opcion("opt_almacenes")
	}
	else if ( this.$titulo.text() == "Unidad de Medida de Articulo") {
		
		this.activar_Arbol("tree_inventarios")
		this.abrir_Submenu("tree_inv_conf")
		this.activar_Opcion("opt_articulo_udm")
	}			
	else if ( this.$titulo.text() == "Articulos") {

		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_articulos")
	}
	else if ( this.$titulo.text() == "Consulta") {

		this.activar_Arbol("tree_trabajos")
		this.activar_Opcion("opt_consulta")
	}
	else if ( this.$titulo.text() == "Ordenes de Trabajo") {

		this.activar_Arbol("tree_trabajos")
		this.activar_Opcion("opt_ordenes")
	}
	else if (this.$titulo.text() == "Todas las Entradas") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_entradas")
		this.activar_Opcion("opt_entradas_todas")
		this.abrir_Submenu("tree_entradas")
	}
	else if (this.$titulo.text() == "Entradas: Saldo Inicial") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_entradas")
		this.activar_Opcion("opt_entradas_saldo")
		this.abrir_Submenu("tree_entradas")
	}
	else if (this.$titulo.text() == "Entradas: Compras") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_entradas")
		this.activar_Opcion("opt_entradas_compras")
		this.abrir_Submenu("tree_entradas")

	}
	else if (this.$titulo.text() == "Entradas: Ajustes") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_entradas")
		this.activar_Opcion("opt_entradas_ajustes")
		this.abrir_Submenu("tree_entradas")
	}
	else if (this.$titulo.text() == "Entradas: Traspaso") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_entradas")
		this.activar_Opcion("opt_entradas_traspasos")
		this.abrir_Submenu("tree_entradas")
	}
	else if (this.$titulo.text() == "Entradas: En Tránsito") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_entradas")
		this.activar_Opcion("opt_entradas_transito")
		this.abrir_Submenu("tree_entradas")
	}
	else if (this.$titulo.text() == "Todas las Salidas") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_salidas")
		this.activar_Opcion("opt_salidas_todas")
		this.abrir_Submenu("tree_salidas")
	}
	else if (this.$titulo.text() == "Salidas: A Personal") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_salidas")
		this.activar_Opcion("opt_salidas_personal")
		this.abrir_Submenu("tree_salidas")
	}
	else if (this.$titulo.text() == "Salidas: Orden de Trabajo") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_salidas")
		this.activar_Opcion("opt_salidas_orden")
		this.abrir_Submenu("tree_salidas")

	}
	else if (this.$titulo.text() == "Salidas: Ajustes") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_salidas")
		this.activar_Opcion("opt_salidas_ajustes")
		this.abrir_Submenu("tree_salidas")

	}
	else if (this.$titulo.text() == "Salidas: Traspaso") {
		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_salidas")
		this.activar_Opcion("opt_salidas_traspasos")
		this.abrir_Submenu("tree_salidas")

	}
	else if ( this.$titulo.text() == "Cardex") {

		this.activar_Arbol("tree_inventarios")
		this.activar_Opcion("opt_todos_mov")
	}
	else if (this.$titulo.text() == "Solicitudes de Compra") {
		this.activar_Arbol("tree_trabajos")
		this.activar_Opcion("opt_materiales")
		this.activar_Opcion("opt_materiales_solicitudes")
		this.abrir_Submenu("tree_trabajos")
	}
	else if (this.$titulo.text() == "Reporte de Necesidades") {
		this.activar_Arbol("tree_trabajos")
		this.abrir_Submenu("tree_trabajos")
		this.activar_Opcion("opt_materiales")
		this.activar_Opcion("opt_materiales_necesidades")
	}	

}
Pagina.prototype.activar_Arbol = function (_tree) {

	var $arbol = $("#" + _tree)
	$arbol.addClass("active")
}
Pagina.prototype.activar_Opcion = function (_option) {

	var $opcion = $("#" + _option)
	$opcion.addClass("active")
}
Pagina.prototype.abrir_Submenu = function (_option) {

	var $opcion = $("#" + _option)
	$opcion.addClass("menu-open")
	$opcion.css('display', 'block')
}
Pagina.prototype.init_Alertify = function () {

    alertify.set('notifier', 'position', 'top-right')
    alertify.set('notifier', 'delay', 10)	

	alertify.defaults.theme.ok = "btn btn-success";
	alertify.defaults.theme.cancel = "btn btn-default";
	alertify.defaults.theme.input = "form-control";
}
Pagina.prototype.get_DatePickerConfig = function () {

	return {
	    autoSize: true,
	    dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
	    dayNamesMin: ['Dom', 'Lu', 'Ma', 'Mi', 'Je', 'Vi', 'Sa'],
	    firstDay: 1,
	    monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
	    monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
	    dateFormat: 'yy-mm-dd',
	    changeMonth: true,
	    changeYear: true,
	}
}


/*-----------------------------------------------*\
            OBJETO: Visor de Mensajes
\*-----------------------------------------------*/

function VisorMensajes() {

	this.$id = $('#mensajes_id')
	this.$perfil = $('#perfil_id')
	this.init()
}
VisorMensajes.prototype.init = function() {
	this.buscar_Mensajes()
}
VisorMensajes.prototype.buscar_Mensajes = function () {

    // Consultamos Mensajes
    $.ajax({
        url: url_mensajes_m,
        method: "GET",
        context: this,
        success: function (response) {
            this.fill(response)
        },
        error: function (response) {
            
            alertify.error("Ocurrio error al consultar las ultimos mensajes")
        }
    })
}
VisorMensajes.prototype.fill = function (_data) {

	var contenido = this.$id
	contenido.empty()

    $.each(_data, function (i, item) {

        var elemento = "<li>" + 
	                    "<a href='mensaje_rev'>" +
	                      "<div class='pull-left'>" +
	                        "<img src= 'usuario_img' class='img-circle' alt='User Image'>"  +
	                      "</div>" +
	                      "<h4>" + 
	                        "<span class='trunc-usuario'>usuario_nombre</span>"  +
	                        "<small><i class='fa fa-clock-o'></i> fecha_creacion</small>"  +
	                      "</h4>"  +
	                      "<p class='trunc-msg'>texto</p>"  +
	                    "</a>" +
	                  "</li>"
    

        new_elemento = elemento.replace("usuario_nombre", item.usuario_nombre)
        new_elemento = new_elemento.replace("texto", item.texto)

        if (item.usuario_img != "") {
            new_elemento = new_elemento.replace("usuario_img", item.usuario_img)
        }
        else {
            new_elemento = new_elemento.replace("usuario_img", "/static/images/decoradores/no-image-user.jpg")
        }
        momento = moment(item.created_date).startOf('min').fromNow()

        new_elemento = new_elemento.replace("fecha_creacion", momento)

        mensaje_rev = url_mensaje_m.replace("mensaje_id", item.pk)

        new_elemento = new_elemento.replace("mensaje_rev", mensaje_rev)

        contenido.append(new_elemento)
    })

	$('.trunc-usuario').succinct({
		size: 15
	})        

	$('.trunc-msg').succinct({
		size: 35
	})    

}
	                  


