/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/


// URLS
var url_udm = window.location.origin + "/api/udmodometro2/"
var url_tipo = window.location.origin + "/api/tipoodometro/"

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

    this.$equipo = $('#id_equipo')
    this.$udm = $("#id_udm")
    this.$tipo = $('#id_tipo')

    this.$boton_editar_udm = $("#btn_edit_udm")

    this.$boton_editar_tipo = $('#btn_edit_tipo')
    this.modal_udm = new VentanaUdm()
    this.modal_tipo = new VentanaTipo()

	this.init()
}
TargetaFormulario.prototype.init = function () {

    this.$equipo.select2()
    this.validar_Udm()
    this.$udm.on("change", this, this.change_Udm)
    this.$tipo.on("change", this, this.change_Tipo)
}
TargetaFormulario.prototype.change_Udm = function (e) {

	if (e.data.$udm.val() == "") {
		e.data.$boton_editar_udm.addClass("disabled")
	}
	else {
		e.data.$boton_editar_udm.removeClass("disabled")
	}
}
TargetaFormulario.prototype.validar_Udm = function () {

	if (this.$udm.val() == "") {
		this.$boton_editar_udm.addClass("disabled")
	}
	else {
		this.$boton_editar_udm.removeClass("disabled")
	}
}
TargetaFormulario.prototype.modify_Udm = function (_clave, _descripcion) {

	var new_value = "(" + _clave + ") " + _descripcion

	// Modificar texto
	this.$udm.find(":selected").text(new_value)
}
TargetaFormulario.prototype.add_Udm = function (_pk, _clave, _descripcion) {
	var new_value = "(" + _clave + ") " + _descripcion

	this.$udm.append(
		$('<option>', {
	    	value: _pk,
	    	text: new_value
		})
	)

	this.$udm.val(_pk)
}
TargetaFormulario.prototype.change_Tipo = function (e) {

    if (e.data.$tipo.val() == "") {
        e.data.$boton_editar_tipo.addClass("disabled")
    }
    else {
        e.data.$boton_editar_tipo.removeClass("disabled")
    }
}
TargetaFormulario.prototype.validar_Tipo = function () {

    if (this.$tipo.val() == "") {
        this.$boton_editar_tipo.addClass("disabled")
    }
    else {
        this.$boton_editar_tipo.removeClass("disabled")
    }
}
TargetaFormulario.prototype.modify_tipo = function (_clave, _descripcion) {

    var new_value = "(" + _clave + ") " + _descripcion

    // Modificar texto
    this.$tipo.find(":selected").text(new_value)
}
TargetaFormulario.prototype.add_Tipo = function (_pk, _clave, _descripcion) {
    var new_value = "(" + _clave + ") " + _descripcion

    this.$tipo.append(
        $('<option>', {
            value: _pk,
            text: new_value
        })
    )

    this.$tipo.val(_pk)
}

/*-----------------------------------------------*\
            OBJETO: Ventana UDM
\*-----------------------------------------------*/

function VentanaUdm() {

	this.$id = $('#win_udm')
	this.$boton_guardar = $('#bnt_udm-save')

	this.$pk = $("#udm_id")
	this.$clave = $('#udm_clave')
	this.$clave_contenedor = $('#udm_clave_contenedor')
	this.$clave_mensaje =  $('#udm_clave_mensaje')

	this.$descripcion =  $('#udm_descripcion')
	this.$desc_contenedor =  $('#udm_desc_contenedor')
	this.$desc_mensaje =  $('#udm_desc_mensaje')

	this.init()
}
VentanaUdm.prototype.init = function () {

	// Se asoscia eventos al abrir el modal
	this.$id.on('show.bs.modal', this, this.load)
}
VentanaUdm.prototype.load = function (e) {

	var event_owner = $(e.relatedTarget)

	// Se eliminan eventos viejos
	e.data.$boton_guardar.off("click")

	// Se limpian estilos
	e.data.clear_Estilos()

	// Se limpiar el formulario
	e.data.clear()	

	// Asosciar Eventos segun corresponda
	if (event_owner.context.id == "btn_new_udm") {

		// Se modifica el titulo
		e.data.$id.find('.modal-title').text('Nueva UDM')
		
		// Se asoscia el evento que se utilizara para guardar
		e.data.$boton_guardar.on(
			"click", 
			e.data, 
			e.data.nuevo
		)
	}
	else if (event_owner.context.id == "btn_edit_udm") {

		// Se llenan los controles
		var url = url_udm + "?id=" + formulario.$udm.val()

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
		e.data.$id.find('.modal-title').text('Editar UDM')

		// Se asoscia el evento que se utilizara para guardar
		e.data.$boton_guardar.on(
			"click", 
			e.data, 
			e.data.editar
		)
	}
}
VentanaUdm.prototype.clear = function () {

	this.$clave.val("")
	this.$descripcion.val("")
}
VentanaUdm.prototype.clear_Estilos = function () {
	
	this.$clave_contenedor.removeClass("has-error")
	
	if(this.$clave_mensaje.hasClass('hidden') != null) { 
		this.$clave_mensaje.addClass('hidden')
	} 

	this.$desc_contenedor.removeClass("has-error")	

	if(this.$desc_mensaje.hasClass('hidden') != null) { 
		this.$desc_mensaje.addClass('hidden')
	} 
}
VentanaUdm.prototype.validar = function () {

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
VentanaUdm.prototype.nuevo = function (e) {

	if (e.data.validar()) {

        $.ajax({
            url: url_udm,
            method: "POST",
            data: {
            	"clave" : e.data.$clave.val(),
            	"descripcion" : e.data.$descripcion.val()
            },
            success: function (response) {

            	e.data.$id.modal('hide')
            	formulario.add_Udm(response.pk, response.clave, response.descripcion)
            },
            error: function (response) {

                alertify.error("Ocurrio error al modificar UDM")
            }
        })
		
	}
}
VentanaUdm.prototype.editar = function (e) {

	if (e.data.validar()) {

		var url_update = url_udm + e.data.$pk.val() + "/"

        $.ajax({
            url: url_update,
            method: "PUT",
            data: {
            	"clave" : e.data.$clave.val(),
            	"descripcion" : e.data.$descripcion.val()
            },
            success: function (response) {

            	e.data.$id.modal('hide')
            	formulario.modify_Udm(e.data.$clave.val(), e.data.$descripcion.val())
            },
            error: function (response) {

                alertify.error("Ocurrio error al modificar UDM")
            }
        })
	}
}

/*-----------------------------------------------*\
            OBJETO: Ventana Tipo
\*-----------------------------------------------*/

function VentanaTipo() {

    this.$id = $('#win_tipo')
    this.$boton_guardar = $('#bnt_tipo-save')

    this.$pk = $("#tipo_id")
    this.$clave = $('#tipo_clave')
    this.$clave_contenedor = $('#tipo_clave_contenedor')
    this.$clave_mensaje =  $('#tipo_clave_mensaje')

    this.$descripcion =  $('#tipo_descripcion')
    this.$desc_contenedor =  $('#tipo_desc_contenedor')
    this.$desc_mensaje =  $('#tipo_desc_mensaje')

    this.init()
}
VentanaTipo.prototype.init = function () {

    // Se asoscia eventos al abrir el modal
    this.$id.on('show.bs.modal', this, this.load)
}
VentanaTipo.prototype.load = function (e) {

    var event_owner = $(e.relatedTarget)

    // Se eliminan eventos viejos
    e.data.$boton_guardar.off("click")

    // Se limpian estilos
    e.data.clear_Estilos()

    // Se limpiar el formulario
    e.data.clear()  

    // Asosciar Eventos segun corresponda
    if (event_owner.context.id == "btn_new_tipo") {

        // Se modifica el titulo
        e.data.$id.find('.modal-title').text('Nuevo Tipo')
        
        // Se asoscia el evento que se utilizara para guardar
        e.data.$boton_guardar.on(
            "click", 
            e.data, 
            e.data.nuevo
        )
    }
    else if (event_owner.context.id == "btn_edit_tipo") {

        // Se llenan los controles
        var url = url_tipo + "?id=" + formulario.$tipo.val()

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
        e.data.$id.find('.modal-title').text('Editar Tipo')

        // Se asoscia el evento que se utilizara para guardar
        e.data.$boton_guardar.on(
            "click", 
            e.data, 
            e.data.editar
        )
    }
}
VentanaTipo.prototype.clear = function () {

    this.$clave.val("")
    this.$descripcion.val("")
}
VentanaTipo.prototype.clear_Estilos = function () {
    
    this.$clave_contenedor.removeClass("has-error")
    
    if(this.$clave_mensaje.hasClass('hidden') != null) { 
        this.$clave_mensaje.addClass('hidden')
    } 

    this.$desc_contenedor.removeClass("has-error")  

    if(this.$desc_mensaje.hasClass('hidden') != null) { 
        this.$desc_mensaje.addClass('hidden')
    } 
}
VentanaTipo.prototype.validar = function () {

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
VentanaTipo.prototype.nuevo = function (e) {

    if (e.data.validar()) {

        $.ajax({
            url: url_tipo,
            method: "POST",
            data: {
                "clave" : e.data.$clave.val(),
                "descripcion" : e.data.$descripcion.val()
            },
            success: function (response) {

                e.data.$id.modal('hide')
                formulario.add_Tipo(response.pk, response.clave, response.descripcion)
            },
            error: function (response) {

                alertify.error("Ocurrio error al modificar UDM")
            }
        })
        
    }
}
VentanaTipo.prototype.editar = function (e) {

    if (e.data.validar()) {

        var url_update = url_tipo + e.data.$pk.val() + "/"

        $.ajax({
            url: url_update,
            method: "PUT",
            data: {
                "clave" : e.data.$clave.val(),
                "descripcion" : e.data.$descripcion.val()
            },
            success: function (response) {

                e.data.$id.modal('hide')
                formulario.modify_tipo(e.data.$clave.val(), e.data.$descripcion.val())
            },
            error: function (response) {

                alertify.error("Ocurrio error al modificar UDM")
            }
        })
    }
}
