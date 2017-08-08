/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_eliminar = window.location.origin + "/api/articulosanexotexto/"

// OBJS
var formulario = null
var item = null


/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function(){
	
	formulario = new TargetaFormulario()
	item = new TargetaItem()
})


/*-----------------------------------------------*\
            OBJETO: Targeta Formulario
\*-----------------------------------------------*/

function TargetaFormulario() {

	this.$textarea = $('#id_texto')

	this.init()
}
TargetaFormulario.prototype.init = function () {

	this.$textarea.wysihtml5();	
}



/*-----------------------------------------------*\
            OBJETO: Targeta Item
\*-----------------------------------------------*/

function TargetaItem() {

	this.init()
}
TargetaItem.prototype.init = function () {

	// aplica evento a todos los items:
	$("[data-action]").on('click', this, this.eliminar)
}
TargetaItem.prototype.eliminar = function (e) {

	var id_anexo = e.currentTarget.dataset.action

	var url = url_eliminar + id_anexo

	$.ajax({
		url: url,
		method: "DELETE",
		success: function (response) {

			e.data.remover(id_anexo)
		},
		error: function(response){
			alertify.error("Ocurrio error al eliminar")
		}                    
	})
}
TargetaItem.prototype.remover = function (_id_anexo) {

	nodo = $("#" + _id_anexo)
	nodo.remove()
}



