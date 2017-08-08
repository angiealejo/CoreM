/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// OBJS
var item = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function(){
    
    formulario = new TargetaFormulario()
})

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

