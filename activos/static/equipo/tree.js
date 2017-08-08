/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_datos = window.location.origin + "/equipos/arbol/json/"

// OBJS
var tree = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    tree = new Arbol()
})


/*-----------------------------------------------*\
            OBJETO: Arbol
\*-----------------------------------------------*/

function Arbol() {

    this.$equipo = $("#equipo_id")
    this.$id = $("#tree")

    this.init()
}
Arbol.prototype.init = function () {

  var url = url_datos + this.$equipo.text() + "/"
  
  $.ajax({
    url: url,
    data: {},
    dataType: "json",
    type: "GET",
    contentType: "application/json; charset=utf-8",
    context: this,
    success: function (_respuesta) {  //--- Se establecio conexion con el servidor

      this.$id.treeview({
        data: _respuesta,
        onNodeSelected: function(e, response) {
            e.preventDefault()
            tree.ver_Equipo(response.clave)
        }
      })
     
    },
    error: function (_respuesta) {
      alertify.error("Fallo")
    }
    // this.FailRequest   //--- Fallo peticion al servidor
  })         
}

Arbol.prototype.ver_Equipo = function (_id) {
  
  url_ver_equipo = window.location.origin + "/equipos/editar/"
  window.location.href = url_ver_equipo + _id + "/"
  
}