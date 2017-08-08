/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/
url_equipo = window.location.origin + "/api/equipoorden/"
var url_datos = window.location.origin + "/equipos/arbol2/json/"

formulario = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

	formulario = new TargetaFormulario()
	modal = new VentanaModal()
})

// Asigna eventos a teclas
$(document).keypress(function (e) {

    // Tecla Enter
    if (e.which == 13) {

        modal.buscar()
    }
})

/*-----------------------------------------------*\
            OBJETO: Targeta Filtros
\*-----------------------------------------------*/

function TargetaFormulario() {

	this.$clave = $('#clave')

	this.$equipo= $("#id_equipo")
	this.$observaciones = $('#id_observaciones')
	this.$motivo_cancelacion = $('#id_motivo_cancelacion')
	this.$responsable = $('#id_responsable')
	this.$solicitante = $('#id_solicitante')

    this.$estado = $('#id_estado')

	this.$fecha_estimada_inicio = $('#id_fecha_estimada_inicio')
	this.$fecha_estimada_fin = $('#id_fecha_estimada_fin')
	this.$fecha_real_inicio = $('#id_fecha_real_inicio')
	this.$fecha_real_fin = $('#id_fecha_real_fin')

	this.$tab_actividades = $("#tab_actividades")
	this.$tab_materiales = $("#tab_materiales")
	this.$tab_servicios = $("#tab_servicios")
	this.$tab_mano_obra = $("#tab_mano_obra")

	this.$boton_arbol = $("#boton_arbol")
	
	this.init()
}
TargetaFormulario.prototype.init = function () {

	this.$equipo.select2()
	this.$responsable.select2()
	this.$solicitante.select2()

	this.$observaciones.wysihtml5({
        toolbar: {
            "link": false,
            "image": false,
            "blockquote": false,
            "font-styles": false,
        },
        customTemplates: this.get_Wysihtml5_Templates()
    })

    this.$motivo_cancelacion.wysihtml5({
        toolbar: {
            "link": false,
            "image": false,
            "blockquote": false,
            "font-styles": false,
        },
        customTemplates: this.get_Wysihtml5_Templates()
    })

    this.$fecha_estimada_inicio.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
	this.$fecha_estimada_inicio.datepicker(this.get_DateConfig())

    this.$fecha_estimada_fin.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
	this.$fecha_estimada_fin.datepicker(this.get_DateConfig())

    this.$fecha_real_inicio.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
	this.$fecha_real_inicio.datepicker(this.get_DateConfig())

    this.$fecha_real_fin.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
	this.$fecha_real_fin.datepicker(this.get_DateConfig())

	this.$tab_actividades.on("click", this, this.click_Tab_Activiades )
	this.$tab_materiales.on("click", this, this.click_Tab_Materiales )
	this.$tab_servicios.on("click", this, this.click_Tab_Servicios )
	this.$tab_mano_obra.on("click", this, this.click_Tab_Mano_Obra )

    this.$estado.on("change", this, this.click_Estado)

	this.deshabilitar_Tabs()
	// this.activar_Tabs()

	this.$boton_arbol.on("click", this, this.click_InputEquipo)
}
TargetaFormulario.prototype.get_Wysihtml5_Templates = function () {

    return {
        emphasis : function(locale) {
            return "<li>" +
                "<div class='btn-group'>" +
                "<a data-wysihtml5-command='bold' title='Bold' class='btn btn-none btn-default' ><span style='font-weight:700'>B</span></a>" +
                "<a data-wysihtml5-command='italic' title='Italics' class='btn btn-none btn-default' ><span style='font-style:italic'>I</span></a>" +
                "<a data-wysihtml5-command='underline' title='Underline' class='btn btn-none btn-default' ><span style='text-decoration:underline'>U</span></a>" +
                "</div>" +
                "</li>";
        },
        lists : function(locale) {
            return "<li>" +
                "<div class='btn-group'>" +
                "<a data-wysihtml5-command='insertUnorderedList' title='Unordered list' class='btn btn-none btn-default' ><span class='fa fa-list-ul'></span></a>" +
                "<a data-wysihtml5-command='insertOrderedList' title='Ordered list' class='btn btn-none btn-default' ><span class='fa fa-list-ol'></span></a>" +
                //"<a data-wysihtml5-command='Outdent' title='Outdent' class='btn btn-none btn-default' ><span class='fa fa-outdent'></span></a>" +
                //"<a data-wysihtml5-command='Indent' title='Indent' class='btn btn-none btn-default'><span class='fa fa-indent'></span></a>" +
                "</div>" +
                "</li>";
        }
    }    
}
TargetaFormulario.prototype.mostrar_MotivoCancelacion = function () {

	// Mostrar

	// Volver obligatorio

	// Centrar la atencion en el campo
}
TargetaFormulario.prototype.ocultar_MotivoCancelacion = function () {

	// Deja de ser obligatorio

	// Se oculta
}
TargetaFormulario.prototype.get_DateConfig = function (){

    return {
        autoclose: true,
        language: 'es',
        todayHighlight: true,
        clearBtn: true,
        startDate: '2017-01-01',
    }
}
TargetaFormulario.prototype.click_InputEquipo = function (e) {
	modal.mostrar()
}
TargetaFormulario.prototype.click_Tab_Activiades = function(e) {

	if (e.data.$clave.text() == ' ') {

		e.preventDefault()
		alertify.warning("Primero debe guardar la Orden")
	}	
}
TargetaFormulario.prototype.click_Tab_Materiales = function(e) {
	if (e.data.$clave.text() == ' ') {

		e.preventDefault()
		alertify.warning("Primero debe guardar la Orden")
	}	
}
TargetaFormulario.prototype.click_Tab_Servicios = function(e) {
	if (e.data.$clave.text() == ' ') {

		e.preventDefault()
		alertify.warning("Primero debe guardar la Orden")
	}	
}
TargetaFormulario.prototype.click_Tab_Mano_Obra = function(e) {
	if (e.data.$clave.text() == ' ') {

		e.preventDefault()
		alertify.warning("Primero debe guardar la Orden")
	}	
}
TargetaFormulario.prototype.deshabilitar_Tabs = function () {
	this.$tab_actividades.attr("data-toggle","")
	this.$tab_materiales.attr("data-toggle","")
	this.$tab_servicios.attr("data-toggle","")
	this.$tab_mano_obra.attr("data-toggle","")
}
TargetaFormulario.prototype.activar_Tabs = function () {
	this.$tab_actividades.attr("data-toggle","tab")
	this.$tab_materiales.attr("data-toggle","tab")
	this.$tab_servicios.attr("data-toggle","tab")
	this.$tab_mano_obra.attr("data-toggle","tab")
}
TargetaFormulario.prototype.llenar_CampoEquipo = function(_id) {
	this.$equipo.val(_id)
	this.$equipo.change()
	//console.log(this.$equipo.val())
}
TargetaFormulario.prototype.click_Estado = function (e) {

    if (this.value == "CAN") {
        // e.data.$motivo_cancelacion.focus()   
        // e.data.$motivo_cancelacion[0].scrollIntoView()

        document.getElementById('id_motivo_cancelacion')
    }
}

/*-----------------------------------------------*\
            OBJETO: Ventana Modal
\*-----------------------------------------------*/

function VentanaModal() {
	this.arbol = new Arbol()
    this.$id = $('#win_modal')
    this.$tag_busqueda = $('#id_tag')
    this.$boton_buscar = $('#boton_buscar')
    this.$boton_seleccionar = $('#btn_modal_seleccionar')
    this.init()

}
VentanaModal.prototype.init = function () {
	this.$boton_buscar.on("click", this, this.click_BotonBuscar)
	this.$boton_seleccionar.on("click", this, this.click_Seleccionar_Item)
}
VentanaModal.prototype.mostrar = function () {

    this.$id.modal('show')
}
VentanaModal.prototype.click_BotonBuscar = function (e) {
	e.preventDefault()
	e.data.buscar()
}
VentanaModal.prototype.buscar = function () {

	if (this.$tag_busqueda.val() != ""){
		data = this.$tag_busqueda.val()
	}
	else{
		data = "PAE"
	}
	modal.arbol.load(data)
}

VentanaModal.prototype.click_Seleccionar_Item = function (e) {
	//console.log(modal.arbol.$id_equipo.val())
	var $nodo = $(".node-selected")
	pk = $nodo.attr('data-clave')
	//console.log(pk)
	formulario.llenar_CampoEquipo(pk)
	e.data.$id.modal('hide')

}


/*-----------------------------------------------*\
            OBJETO: Arbol
\*-----------------------------------------------*/

function Arbol () {

	this.$id = $('#tree')
	this.$id_equipo = $('#equipo')
    this.$tag = $('#tag')
    this.$descripcion = $('#descripcion')
    this.$separador = $('#separador')
}
Arbol.prototype.load = function (_pk) {
	var url = url_datos + _pk + "/"
	//console.log(_pk)
	  $.ajax({
	    url: url,
	    data: {},
	    dataType: "json",
	    type: "GET",
	    contentType: "application/json; charset=utf-8",
	    context: this,
	    success: function (_respuesta) { 
	    	//console.log(_respuesta)
	      this.$id.treeview({
	        data: _respuesta,
	        selectedBackColor: '#1D9744',
	      })

	      this.$id.treeview(
	      	'collapseAll', { silent: true 
	      })
	     
	    },
	    error: function (_respuesta) {
	      alertify.error("Fallo")
	    }
	    
	  })  
}
Arbol.prototype.set_Text = function (_tag, _sep, _desc, _id) {
	this.$id_equipo.val(_id)
	this.$tag.text(_tag)
	this.$separador.text(_sep)
	this.$descripcion.text(_desc)
	
}