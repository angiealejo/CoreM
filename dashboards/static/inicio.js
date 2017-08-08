 /*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_last_ordenes = window.location.origin + "/api/ordenestrabajolast/"
var url_ordenes_abiertas = window.location.origin + "/ordenestrabajoabiertas/"
var url_ordenes_terminadas = window.location.origin + "/ordenestrabajoterminadas/"
var url_entradas_transito = window.location.origin + "/entradastransito/"

var url_mensajes = window.location.origin + "/api/mensajes/"
var url_usuario = window.location.origin + "/api/users/usuario_id/"
var url_perfil = "/usuarios/perfil/usuario_id/"

// OBJS
var box_ordenes = null
var last_ordenes = null
var mensajes = null

var calendar = null
var grafica_costos = null



/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

	box_ordenes = new BoxOrdenes()
	last_ordenes = new ListOrdenes()
    mensajes = new Chat()

})


/*-----------------------------------------------*\
            OBJETO: RESUMEN DOCUMENTOS
\*-----------------------------------------------*/

function BoxOrdenes () {
	this.$ordenes_abiertas = $('#id_ordenes_abiertas')
	this.$ordenes_terminadas = $('#id_ordenes_terminadas')
	this.$entradas_transito = $('#id_entradas_transito')
	this.init()
}
BoxOrdenes.prototype.init = function () {
	this.set_OrdenTerminada()
	this.set_OrdenAbierta()
	this.set_EntradaTransito()
}
BoxOrdenes.prototype.set_OrdenTerminada = function () {
	$.ajax({
        url: url_ordenes_terminadas,
        method: "GET",
        context: this,
        success: function (response) {
        	this.$ordenes_terminadas.text(response.data)
        },
        error: function (response) {
            
            alertify.error("Error al consultar órdenes terminadas")
        }
    })
}
BoxOrdenes.prototype.set_OrdenAbierta = function () {
	$.ajax({
        url: url_ordenes_abiertas,
        method: "GET",
        context: this,
        success: function (response) {
        	this.$ordenes_abiertas.text(response.data)	
        },
        error: function (response) {
            
            alertify.error("Error al consultar órdenes abiertas")
        }
    })
}
BoxOrdenes.prototype.set_EntradaTransito = function () {
	$.ajax({
        url: url_entradas_transito,
        method: "GET",
        context: this,
        success: function (response) {
        	this.$entradas_transito.text(response.data)	
        },
        error: function (response) {
            
            alertify.error("Error al consultar entradas en transito")
        }
    })
}


/*-----------------------------------------------*\
            OBJETO: ULTIMAS ORDENES
\*-----------------------------------------------*/

function ListOrdenes() {

	this.$contenido = $('#tabla_contenido')

	this.init()
}
ListOrdenes.prototype.init = function () {

	// Consultamos Ordenes
    $.ajax({
        url: url_last_ordenes,
        method: "GET",
        context: this,
        success: function (response) {
        	this.fill_Contenido(response)
        },
        error: function (response) {
            
            alertify.error("Ocurrio error al consultar las ultimas ordenes")
        }
    })
}
ListOrdenes.prototype.fill_Contenido = function (_data) {

	var tabla_contenio = this.$contenido

	$.each(_data, function (i, item) {

		var url_editar_orden = tabla_contenio.data("ordenes")
		var url_editar_equipo = tabla_contenio.data("equipos")

		var url_ordenes = url_editar_orden.replace("0", item.pk)
		var url_equipos = url_editar_equipo.replace("0", item.equipo_id)

		var clase_estado = ""

		if (item.estado == "ABIERTA") {
			clase_estado = "label-success"
		}
		else if (item.estado == "TERMINADA") {
			clase_estado = "label-info"
		}
		else if (item.estado == "CERRADA") {
			clase_estado = "label-default"
		}
        else if (item.estado == "CANCELADA") {
            clase_estado = "bg-yellow"
        }        
		else if (item.estado == "PENDIENTE") { 
			clase_estado = "label-warning"
		}

		var elemento = "<tr>" +
			"<td><a href='#'><span class='badge'>clave</span></a></td>".replace("clave", item.pk).replace('#', url_ordenes) +
			"<td><a href='#'>descripcion</td></a>".replace("descripcion", item.descripcion).replace('#', url_ordenes) +
            "<td>responsable</td>".replace("responsable", item.responsable) +
			"<td><a href='#'>equipo</a></td>".replace("equipo", item.equipo).replace('#', url_equipos) +
			"<td><span class='label label-color'>estado</span></td>".replace("estado", item.estado).replace("label-color", clase_estado) +
		"</tr>"

		tabla_contenio.append(elemento)
	})
}

/*-----------------------------------------------*\
            OBJETO: Chat
\*-----------------------------------------------*/

function Chat() {

	this.$id = $('#chat-box')
    this.$caja_mensaje = $('#caja_mensaje')
    this.$boton_agregar = $('#boton_agregar')
    this.$perfil = $('#perfil_id')
	this.init()
}
Chat.prototype.init = function () {

    this.set_Altura()
    this.buscar_Mensajes()

    this.$boton_agregar.on("click", this, this.agregar_Mensaje)
}
Chat.prototype.set_Altura = function () {

    this.$id.slimScroll({
        height: '350px'
    })
}
Chat.prototype.buscar_Mensajes = function () {

    // Consultamos Mensajes
    $.ajax({
        url: url_mensajes,
        method: "GET",
        context: this,
        success: function (response) {
            this.fill(response)
        },
        error: function (response) {
            
            alertify.error("Ocurrio error al consultar los ultimos mendajes")
        }
    })    
}
Chat.prototype.fill = function (_data) {

    var contenido = this.$id
    contenido.empty()
    
    $.each(_data, function (i, item) {

        var elemento = "<div class='item'>" + 
                        "<img src= 'usuario_img' alt='user image' class='offline'>" +
                        "<p class='message'>"  + 
                            "<a href='usuario_perfil' class='name'>"  + 
                                "<small class='text-muted pull-right'><i class='fa fa-clock-o'></i> fecha_creacion</small>"  + 
                                "usuario_nombre"  + 
                            "</a>"  + 
                            "texto"  + 
                        "</p>"  + 
                       "</div>"        

        new_elemento = elemento.replace("usuario_nombre", item.usuario_nombre)
        new_elemento = new_elemento.replace("texto", item.texto)

        if (item.usuario_img != "") {
            new_elemento = new_elemento.replace("usuario_img", item.usuario_img)
        }
        else {
            new_elemento = new_elemento.replace("usuario_img", "/static/images/decoradores/no-image-user.jpg")
        }

        moment.locale('es')
        momento = moment(item.created_date).startOf('min').fromNow()

        new_elemento = new_elemento.replace("fecha_creacion", momento)

        perfil = url_perfil.replace("usuario_id", item.usuario_id)
        new_elemento = new_elemento.replace("usuario_perfil", perfil)

        contenido.append(new_elemento)
    })
}
Chat.prototype.agregar_Mensaje = function(e) {

    var usuario = url_usuario.replace("usuario_id", e.data.$perfil.data("clave")) 
    var text = e.data.$caja_mensaje.val()

    var obj = e.data

    if (text != "" ) {

        $.ajax({
            url: url_mensajes,
            data: {
                "usuario" : usuario,
                "texto" : text
            },
            method: "POST",
            context: this,
            success: function (response) {

                alertify.warning("Se envio mensaje")
                obj.$caja_mensaje.val("")
                obj.buscar_Mensajes()
                view_mensajes.buscar_Mensajes()
            },
            error: function (response) {
                
                alertify.error("Ocurrio error al enviar mensaje")
            }
        })
    }
}

