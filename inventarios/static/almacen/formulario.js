/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    formulario = new Formulario()
})

/*-----------------------------------------------*\
            OBJETO: FORMULARIO
\*-----------------------------------------------*/

function Formulario() {

    this.$id = $("#id_formulario")

    this.$boton_guardar = $("#boton_guardar")

    this.init()
}
Formulario.prototype.init = function () {

    this.$id.on("submit", this, this.click_deshabilitar_Boton)

}

Formulario.prototype.click_deshabilitar_Boton = function (e) {

    e.data.$boton_guardar.attr("disabled", true)

}