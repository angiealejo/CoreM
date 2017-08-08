/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_ubicaciones = window.location.origin + "/api/ubicaciones2/"
// var url_equipos = window.location.origin + "/api/equipos/"

// OBJS
var formulario = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    formulario = new TargetaFormulario() 
})


/*-----------------------------------------------*\
            OBJETO: Targeta Formulario
\*-----------------------------------------------*/

function TargetaFormulario() {

    this.$padre = $('#id_padre')
    this.$id = $('#id_equipo')
    this.$responsable = $('#id_responsable')
    this.$ubicacion = $("#id_ubicacion")
    this.$contrato = $('#id_contrato')
    
    this.$imagen = $('#id_imagen')
	this.$imagen_preview = $('#img_preview')

    this.$boton_editar_ubicacion = $("#btn_edit_ubicacion")
    this.$boton_guardar = $('#boton_guardar')
    this.modal_ubicacion = new VentanaUbicacion()

	this.init()
}
TargetaFormulario.prototype.init = function () {

	this.$imagen.on("change",this, this.set_PreviewImagen)

    this.$padre.select2()
    this.$responsable.select2()
    this.$contrato.select2()

    this.validar_Ubicacion()
    this.$ubicacion.on("change", this, this.change_Ubicacion)
    this.$padre.on("change", this, this.validar_Padre)
}
TargetaFormulario.prototype.set_PreviewImagen = function (e) {

    if (this.files && this.files[0]) {
        
        var reader = new FileReader()

        reader.onload = function (e) {
            formulario.$imagen_preview.attr('src', e.target.result)
        }

        reader.readAsDataURL(this.files[0])

    }
}
TargetaFormulario.prototype.change_Ubicacion = function (e) {

	if (e.data.$ubicacion.val() == "") {
		e.data.$boton_editar_ubicacion.addClass("disabled")
	}
	else {
		e.data.$boton_editar_ubicacion.removeClass("disabled")
	}
}
TargetaFormulario.prototype.validar_Ubicacion = function () {

	if (this.$ubicacion.val() == "") {
		this.$boton_editar_ubicacion.addClass("disabled")
	}
	else {
		this.$boton_editar_ubicacion.removeClass("disabled")
	}
}
TargetaFormulario.prototype.modify_Ubicacion = function (_clave, _descripcion) {

	var new_value = "(" + _clave + ") " + _descripcion

	// Modificar texto
	this.$ubicacion.find(":selected").text(new_value)
}
TargetaFormulario.prototype.add_Ubicacion = function (_pk, _clave, _descripcion) {
	var new_value = "(" + _clave + ") " + _descripcion

	this.$ubicacion.append(
		$('<option>', {
	    	value: _pk,
	    	text: new_value
		})
	)

	this.$ubicacion.val(_pk)
}
TargetaFormulario.prototype.validar_Padre = function (e) {

	var equipo_id = e.data.$id.val()
	padre_id = e.data.$padre.val()
	if (padre_id == equipo_id){
		e.data.$boton_guardar.attr("disabled", true)
		alertify.error("El padre no puede ser el mismo equipo")
	}
	else{
		e.data.$boton_guardar.attr("disabled", false)
	}

	
}

/*-----------------------------------------------*\
            OBJETO: Ventana Ubicacion
\*-----------------------------------------------*/

function VentanaUbicacion() {

	this.$id = $('#win_ubicacion')
	this.$boton_guardar = $('#bnt_ubi-save')

	this.$pk = $("#ubi_id")
	this.$clave = $('#ubi_clave')
	this.$clave_contenedor = $('#ubi_clave_contenedor')
	this.$clave_mensaje =  $('#ubi_clave_mensaje')

	this.$descripcion =  $('#ubi_descripcion')
	this.$desc_contenedor =  $('#ubi_desc_contenedor')
	this.$desc_mensaje =  $('#ubi_desc_mensaje')

	this.init()
}
VentanaUbicacion.prototype.init = function () {

	// Se asoscia eventos al abrir el modal
	this.$id.on('show.bs.modal', this, this.load)
}
VentanaUbicacion.prototype.load = function (e) {

	var event_owner = $(e.relatedTarget)

	// Se eliminan eventos viejos
	e.data.$boton_guardar.off("click")

	// Se limpian estilos
	e.data.clear_Estilos()

	// Se limpiar el formulario
	e.data.clear()	

	// Asosciar Eventos segun corresponda
	if (event_owner.context.id == "btn_new_ubicacion") {

		// Se modifica el titulo
		e.data.$id.find('.modal-title').text('Nueva Ubicacion')
		
		// Se asoscia el evento que se utilizara para guardar
		e.data.$boton_guardar.on(
			"click", 
			e.data, 
			e.data.nuevo
		)
	}
	else if (event_owner.context.id == "btn_edit_ubicacion") {

		// Se llenan los controles
		var url = url_ubicaciones + "?id=" + formulario.$ubicacion.val()

		modal = e.data

        $.ajax({
            url: url,
            method: "GET",
            success: function (response) {

            	modal.$pk.val(response[0].pk)
                modal.$clave.val(response[0].clave)
                modal.$descripcion.val(response[0].descripcion)
            },
            error: function (response) {
                
                alertify.error("Ocurrio error al consultar")
            }
        })

		// Se modifica el titulo
		e.data.$id.find('.modal-title').text('Editar Ubicacion')

		// Se asoscia el evento que se utilizara para guardar
		e.data.$boton_guardar.on(
			"click", 
			e.data, 
			e.data.editar
		)
	}
}
VentanaUbicacion.prototype.clear = function () {

	this.$clave.val("")
	this.$descripcion.val("")
}
VentanaUbicacion.prototype.clear_Estilos = function () {
	
	this.$clave_contenedor.removeClass("has-error")
	
	if(this.$clave_mensaje.hasClass('hidden') != null) { 
		this.$clave_mensaje.addClass('hidden')
	} 

	this.$desc_contenedor.removeClass("has-error")	

	if(this.$desc_mensaje.hasClass('hidden') != null) { 
		this.$desc_mensaje.addClass('hidden')
	} 
}
VentanaUbicacion.prototype.validar = function () {

	var bandera = true

	if ( this.$clave.val() == "") {
		this.$clave_contenedor.addClass("has-error")
		this.$clave_mensaje.removeClass("hidden")
		bandera = false
	}

	if ( this.$descripcion.val() == "") {
		this.$desc_contenedor.addClass("has-error")
		this.$desc_mensaje.removeClass("hidden")
		bandera = false
	}

	return bandera
}
VentanaUbicacion.prototype.nuevo = function (e) {

	if (e.data.validar()) {

        $.ajax({
            url: url_ubicaciones,
            method: "POST",
            data: {
            	"clave" : e.data.$clave.val(),
            	"descripcion" : e.data.$descripcion.val()
            },
            success: function (response) {

            	e.data.$id.modal('hide')
            	formulario.add_Ubicacion(response.pk, response.clave, response.descripcion)
            },
            error: function (response) {

                alertify.error("Ocurrio error al modificar Ubicacion")
            }
        })
		
	}
}
VentanaUbicacion.prototype.editar = function (e) {

	if (e.data.validar()) {

		var url_update = url_ubicaciones + e.data.$pk.val() + "/"

        $.ajax({
            url: url_update,
            method: "PUT",
            data: {
            	"clave" : e.data.$clave.val(),
            	"descripcion" : e.data.$descripcion.val()
            },
            success: function (response) {

            	e.data.$id.modal('hide')
            	formulario.modify_Ubicacion(e.data.$clave.val(), e.data.$descripcion.val())
            },
            error: function (response) {

                alertify.error("Ocurrio error al modificar Ubicacion")
            }
        })
	}
}
