// OBJS
var formulario = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    formulario = new TargetaFormulario() 
})

function TargetaFormulario () {

	this.$logo = $('#id_logo')
	this.$imagen_preview = $('#img_preview')
	this.init()
}
TargetaFormulario.prototype.init = function () {
	this.$logo.on("change",this, this.set_PreviewImagen)
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