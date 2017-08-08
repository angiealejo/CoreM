/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_eliminar = window.location.origin + "/api/actividaddetalles/"

// OBJS
var item = null


/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function(){
	
	item = new TargetaItem()
	formulario = new TargetaFormulario()
})



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

/*-----------------------------------------------*\
            OBJETO: Targeta Formularo
\*-----------------------------------------------*/

function TargetaFormulario() {

	this.$textarea = $('#id_comentarios')

	this.init()
}
TargetaFormulario.prototype.init = function () {

    this.$textarea.wysihtml5({
        toolbar: {
            "link": false,
            "image": false,
            "blockquote": false,
            "font-styles": false,
        },
        customTemplates: this.get_Wysihtml5_Templates()
    })  
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

