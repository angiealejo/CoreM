/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/


// URLS
var url_materiales = window.location.origin + "/api/materiales/"
var url_ordenes = window.location.origin + "/api/ordenestrabajo/"
var url_articulos = window.location.origin + "/api/articulos2/"
var url_articulos1 = window.location.origin + "/api/articulos/"
var url_stock = window.location.origin + "/api/stockexcel/"
var url_mostrar_stock = window.location.origin + "/stock/"
// OBJS
var targeta_resultados = null
var $ot_clave = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    $ot_clave = $('#ot_clave')

    targeta_resultados = new TargetaResultados()

    if (targeta_resultados.grid.$permiso.val() != "autenticado"){
        targeta_resultados.toolbar.ocultar_BotonNuevo()
        targeta_resultados.grid.ocultar_Botones()
    }
})


/*-----------------------------------------------*\
            OBJETO: RESULTADOS
\*-----------------------------------------------*/

function TargetaResultados() {

    this.toolbar = new Toolbar()
    this.grid = new GridPrincipal()
    this.modal = new VentanaModal()
}


/*-----------------------------------------------*\
            OBJETO: GRID
\*-----------------------------------------------*/

function GridPrincipal() {

	this.$id = $("#grid_principal")
    this.$permiso = $('#id_permiso')
    this.$botones_editar = null
    this.kfuente_datos = null
    this.kgrid = null

    this.init()
}
GridPrincipal.prototype.init = function () {
    
	kendo.culture("es-MX")

    this.kfuente_datos = new kendo.data.DataSource(this.get_FuenteDatosConfig())

    this.kgrid = this.$id.kendoGrid(this.get_Config())

}
GridPrincipal.prototype.ocultar_Botones = function () {

    var grid = this.kgrid.data("kendoGrid")
    grid.hideColumn(4)
}
GridPrincipal.prototype.get_Config = function () {

    return {
        dataSource: this.kfuente_datos,
        columnMenu: false,
        groupable: false,
        sortable: false,
        editable: false,
        resizable: true,
        selectable: true,
        scrollable: false,
        columns: this.get_Columnas(),
        scrollable: true,
        noRecords: {
            template: "<div class='grid-empy'> No se encontraron registros </div>"
        },
        dataBound: this.apply_Estilos
    }
}
GridPrincipal.prototype.get_Campos = function (e) {

    return {
        articulo : { type:"string" },
        articulo_desc : { type:"string" },
        articulo_udm : { type:"string" },
        cantidad_estimada : { type: "number" },
        cantidad_real : { type: "number" },
    }
}

GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { field: "articulo_desc", title: "Articulo", width: "400px" },
        { field: "cantidad_estimada", title: "Cantidad Estimada", width: "130px", format: '{0:n2}'},
        { field: "cantidad_real", title: "Cantidad Real", width: "130px", format: '{0:n2}'},
        { field: "articulo_udm", title: "Unidad de Medida", width: "150px",},        
        {
           command: [
                {
                   text: " Editar",
                   click: this.click_BotonEditar,
                   className: "boton_editar fa fa-pencil"
                },
                {
                   text: " Stock",
                   click: this.click_BotonStock,
                   className: "boton_default fa fa-th-large"
                },   
                {
                    text: " Eliminar",
                    click: this.click_BotonEliminar,
                    className: "boton_eliminar fa fa-trash-o"
                },                
            ],           
           title: " ",
           width: "300px"
        },
    ]
}
GridPrincipal.prototype.apply_Estilos = function (e) {

    // Aplicar iconos
    e.sender.tbody.find(".k-button.fa.fa-pencil").each(function(idx, element){
        $(element).removeClass("fa fa-pencil").find("span").addClass("fa fa-pencil")
    })
    e.sender.tbody.find(".k-button.fa.fa-th-large").each(function(idx, element){
        $(element).removeClass("fa fa-th-large").find("span").addClass("fa fa-th-large")
    })

    e.sender.tbody.find(".k-button.fa.fa-trash-o").each(function(idx, element){
        $(element).removeClass("fa fa-trash-o").find("span").addClass("fa fa-trash-o")
    })
}
GridPrincipal.prototype.get_FuenteDatosConfig = function (e) {

    return {
        transport: {
            read: {
                url: url_materiales,
                type: "GET",
                dataType: "json",
            },
            parameterMap: function (data, action) {
                if (action === "read") {

                    return {
                        orden: $ot_clave.text()
                    }
                }
            }
        },
        schema: {
            model: {
                fields: this.get_Campos()
            }
        },
        error: function (e) {
            alertify.error("Status: " + e.status + "; Error message: " + e.errorThrown)
        },
    }
}
GridPrincipal.prototype.buscar = function() {
    this.kfuente_datos.read()
}
GridPrincipal.prototype.click_BotonEditar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    var clave_articulo = fila.pk
    targeta_resultados.modal.set_Id(clave_articulo.toString())
    targeta_resultados.modal.mostrar()
}
GridPrincipal.prototype.click_BotonStock = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_mostrar_stock + "0/" + fila.articulo_id + "/"
}
GridPrincipal.prototype.click_BotonEliminar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))

    alertify.confirm(
        'Eliminar Registro',
        '¿Desea Eliminar este registro?', 
        function () {

            var url = url_materiales + fila.pk + "/"

            $.ajax({
                url: url,
                method: "DELETE",
                success: function () {
                    alertify.success("Se elimino registro correctamente")
                    
                    targeta_resultados.grid.kfuente_datos.remove(fila)

                },
                error: function () {
                    
                    alertify.error("Ocurrio un error al eliminar")
                }
            })
        }, 
        null
    )    
}

/*-----------------------------------------------*\
            OBJETO: TOOLBAR
\*-----------------------------------------------*/

function Toolbar() {

    this.$boton_nuevo = $("#boton_nuevo")

    this.init()
}
Toolbar.prototype.init = function (e) {

    //this.$boton_exportar.on("click", this, this.click_BotonExportar)
}

Toolbar.prototype.ocultar_BotonNuevo = function () {
    this.$boton_nuevo.addClass("hidden")
}


/*-----------------------------------------------*\
            OBJETO: Ventana Modal
\*-----------------------------------------------*/

function VentanaModal() {

    this.$id = $('#win_modal')

    this.$pk = $("#mat_id")

    this.$articulo = $('#mat_articulo')
    this.$articulo_contenedor = $('#mat_articulo_contenedor')
    this.$articulo_mensaje =  $('#mat_articulo_mensaje')

    this.$cantidad_estimada =  $('#mat_cant_esti')
    this.$cant_est_contenedor =  $('#mat_cant_esti_contenedor')
    this.$cant_est_mensaje =  $('#mat_cant_esti_mensaje')

    this.$boton_guardar = $('#btn_modal_save')

    this.init()
}
VentanaModal.prototype.init = function () {

    // Se aplican componentes
    this.$articulo.select2()

    // Se asoscia eventos al abrir el modal
    this.$id.on('show.bs.modal', this, this.load)
}
VentanaModal.prototype.set_Id = function (_value) {

    this.$pk.val(_value)
}
VentanaModal.prototype.mostrar = function (e) {
    this.$id.modal()
}
VentanaModal.prototype.clear_Fields = function () {

    this.$articulo.empty()
    this.$cantidad_estimada.val("")
}
VentanaModal.prototype.clear_Estilos = function () {
    
    this.$articulo_contenedor.removeClass("has-error")
    
    if(this.$articulo_mensaje.hasClass('hidden') != null) { 
        this.$articulo_mensaje.addClass('hidden')
    } 

    this.$cant_est_contenedor.removeClass("has-error")  

    if(this.$cant_est_mensaje.hasClass('hidden') != null) { 
        this.$cant_est_mensaje.addClass('hidden')
    } 
}
VentanaModal.prototype.validar = function () {

    var bandera = true

    if ( this.$articulo.val() == "") {
        this.$articulo_contenedor.addClass("has-error")
        this.$articulo_mensaje.removeClass("hidden")
        bandera = false
    }

    if ( this.$cantidad_estimada.val() == "") {
        this.$cant_est_contenedor.addClass("has-error")
        this.$cant_est_mensaje.removeClass("hidden")
        bandera = false
    }

    return bandera
}
VentanaModal.prototype.fill_Articulos = function (_value, _selected) {

    combo_articulos = this.$articulo

    // Obtenemos articulos
    $.ajax({
        url: url_articulos,
        data: {
            "estado" :  _value
        },
        method: "GET",
        success: function (response) {

            combo_articulos.append($('<option>', { 
                value: 0,
                text : "-----------"
            }))            

            $.each(response, function (i, item) {
                if (item.clave == null | item.clave ==""){
                    clave = "-"
                }
                else{
                    clave = item.clave
                }
                 combo_articulos.append($('<option>', { 
                    value: item.pk,
                    text : item.informacion,
                }))
            })

            combo_articulos.trigger('change')

            combo_articulos.val(_selected).trigger('change')
        },
        error: function (response) {
            
            alertify.error("Ocurrio error al consultar")
        }
    })    
}
VentanaModal.prototype.load = function (e) {

    // Se eliminan eventos viejos
    e.data.$boton_guardar.off("click")

    // Se limpian estilos
    e.data.clear_Estilos()

    // Se limpiar el formulario
    e.data.clear_Fields()  

    // Asosciar Eventos segun corresponda
    var event_owner

    // Edicion
    if ( e.relatedTarget == undefined ) {

        // Se modifica el titulo
        e.data.$id.find('.modal-title').text('Editar Material Agregado')

        modal = e.data

        $.ajax({
            url: url_materiales,
            method: "GET",
            data: {
                "id": e.data.$pk.val()
            },
            success: function (response) {

                // modal.$articulo.val(response[0].articulo)
                modal.$cantidad_estimada.val(response[0].cantidad_estimada)

                modal.fill_Articulos("", response[0].articulo_id)
            },
            error: function (response) {
                
                alertify.error("Ocurrio error al consultar")
            }
        })
        // Se asoscia el evento que se utilizara para guardar
        e.data.$boton_guardar.on(
            "click", 
            e.data, 
            e.data.editar
        )        
    }
    // Agregar
    else {

        e.data.fill_Articulos("ACT")

        event_owner = $(e.relatedTarget) 

        if (event_owner.context.id == "boton_nuevo") {

            // Se modifica el titulo
            e.data.$id.find('.modal-title').text('Agregar Material')
            
            // Se asoscia el evento que se utilizara para guardar
            e.data.$boton_guardar.on(
                "click", 
                e.data, 
                e.data.nuevo
            )
        }        
    }
}
VentanaModal.prototype.nuevo = function (e) {

    if (e.data.validar()) {

        $.ajax({
            url: url_materiales,
            method: "POST",
            data: {
                "orden" :  url_ordenes + $ot_clave.text() + "/",
                "articulo" : url_articulos1 + e.data.$articulo.val() + "/",
                "cantidad_estimada" : e.data.$cantidad_estimada.val(),
            },
            success: function (response) {

                targeta_resultados.grid.kfuente_datos.read()

                // Ocultar Modal
                e.data.$id.modal('hide')

            },
            error: function (response) {

                if (response.readyState == 4 && response.status == 500) {
                    alertify.error("El registro ya existe en la BD")
                }
                else {
                    alertify.error("Ocurrio error al modificar registro")
                }
            }
        })
    }
}
VentanaModal.prototype.editar = function (e) {

    if (e.data.validar()) {

        var url_update = url_materiales + e.data.$pk.val() + "/"

        $.ajax({
            url: url_update,
            method: "PUT",
            data: {
                "orden" :  url_ordenes + $ot_clave.text() + "/",
                "articulo" : url_articulos1 + e.data.$articulo.val() + "/",
                "cantidad_estimada" : e.data.$cantidad_estimada.val(),
            },
            success: function (response) {

                targeta_resultados.grid.kfuente_datos.read()

                e.data.$id.modal('hide')
            },
            error: function (response) {

                if (response.readyState == 4 && response.status == 500) {
                    alertify.error("El registro ya existe en la BD")
                }
                else {
                    alertify.error("Ocurrio error al modificar registro")
                }
            }
        })
    }
}
