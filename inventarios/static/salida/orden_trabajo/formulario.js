/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_grid = window.location.origin + "/api/movimientosdetalle/"
var url_detalle_excel = window.location.origin + "/api/movimientosdetalleexcel/"
var url_articulos = window.location.origin + "/api/articulosforordenes/"
var url_stock = window.location.origin + "/stock/"
var url_ordenes = window.location.origin + "/api/ordenestrabajo/"
var url_almacenes = window.location.origin + "/api/almacenes2/"

var url_articulos_upd = window.location.origin + "/api/articulos/articulo_id/"
var url_cabecera_upd = window.location.origin + "/api/movimientos/cabecera_id/"


// OBJS
var targeta_filtros = null
var targeta_resultados = null
var modal_detalle = null
var pagina = null


/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    targeta_filtros = new TargetaFormulario()

    // Se inicializan los objetos si es necesario
    if (targeta_filtros.$cabecera != "") {
        
        targeta_resultados = new TargetaResultados()
        modal_detalle = new ModalDetalle()

        if (targeta_filtros.$estado.val() == "CERRADO"){
            targeta_filtros.deshabilitar_Campos()
            targeta_resultados.toolbar.deshabilitar_Campos()
            targeta_resultados.grid.ocultar_Botones()
        }

    }
    

})

/*-----------------------------------------------*\
            OBJETO: Targeta Formulario
\*-----------------------------------------------*/

function TargetaFormulario() {

    this.$id = $('#id_panel')
    this.$operacion = $('#operacion')
    this.$estado = $('#id_estado')
    this.$cabecera = $('#id_cabecera')
    this.$descripcion = $('#id_descripcion')
    this.$fecha = $('#id_fecha')
    this.$almacen_origen = $('#id_almacen_origen')
    this.$orden_trabajo = $('#id_orden_trabajo')
    this.$persona_recibe = $('#id_persona_recibe')
    this.$persona_entrega = $('#id_persona_entrega')
    this.$boton_guardar = $('#boton_guardar')

    this.init()
}
TargetaFormulario.prototype.init = function () {
    this.$almacen_origen.select2()
    this.$persona_recibe.select2()
    this.$persona_entrega.select2()
    this.$orden_trabajo.select2()
    this.$fecha.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha.datepicker(
        {
            autoclose: true,
            language: 'es',
            todayHighlight: true,
            clearBtn: true,
            startDate: '2017-01-01',
        }
    ) 

    this.$orden_trabajo.on('change', this, this.validar_Orden)
    this.$almacen_origen.on('change', this, this.validar_Almacen)
    
}
TargetaFormulario.prototype.validar_Orden = function (e) {
    $.ajax({
            url: url_ordenes,
            method: "GET",
            data: {
                "id": targeta_filtros.$orden_trabajo.val()
            },
            success: function (response) {

                if(response.results[0].estado!="CERRADA"){
                    e.data.$boton_guardar.attr("disabled", false)
                }
                else{
                    e.data.$boton_guardar.attr("disabled", true)
                    alertify.error("Orden Cerrada. Seleccione otra orden.")
                }

            },
            error: function () {

                alertify.error("Ocurrió un error al consultar")
            }
    })
}
TargetaFormulario.prototype.validar_Almacen = function (e) {
    $.ajax({
            url: url_almacenes,
            method: "GET",
            data: {
            "id": targeta_filtros.$almacen_origen.val()
            },
            success: function (response) {
                $.each(response, function (index, item){
                    if(item.estado!="DESHABILITADO"){
                        e.data.$boton_guardar.attr("disabled", false)
                    }
                    else{
                        e.data$boton_guardar.attr("disabled", true)
                        alertify.error("Almacen Deshabilitado.")
                    }
                })
            },
            error: function () {

                alertify.error("Ocurrió un error al consultar")
            }
    })
    
}
TargetaFormulario.prototype.deshabilitar_Campos = function () {
   
        this.$descripcion.attr("disabled", true)
        this.$fecha.attr("disabled", true)
        this.$almacen_origen.attr("disabled", true)
        this.$orden_trabajo.attr("disabled", true)
        this.$persona_entrega.attr("disabled", true)
        this.$persona_recibe.attr("disabled", true)
        this.$boton_guardar.attr("disabled", true)

}
TargetaFormulario.prototype.get_Filtros = function (_page, _pageSize) {

    return {
        page: _page,
        pageSize: _pageSize,
        cabecera: this.$cabecera.val(),

    }
}

/*-----------------------------------------------*\
            OBJETO: RESULTADOS
\*-----------------------------------------------*/

function TargetaResultados() {

    this.toolbar = new Toolbar()
    this.grid = new GridPrincipal()
}


/*-----------------------------------------------*\
            OBJETO: GRID
\*-----------------------------------------------*/

function GridPrincipal() {

    this.$id = $("#grid_principal")
    this.kfuente_datos = null
    this.kgrid = null

    this.init()
}
GridPrincipal.prototype.init = function () {

    kendo.culture("es-MX")

    this.kfuente_datos = new kendo.data.DataSource(this.get_FuenteDatosConfig())
    this.kfuente_datos_excel = new kendo.data.DataSource(this.get_FuenteDatosConfigExcel())

    if (targeta_filtros.$estado.val() == "CERRADO"){
        this.kgrid = this.$id.kendoGrid(this.get_Config_Disable())
    }
    else {
        this.kgrid = this.$id.kendoGrid(this.get_Config())
    }
}
GridPrincipal.prototype.get_Config = function () {

    return {
        dataSource: this.kfuente_datos,
        columnMenu: false,
        groupable: false,
        sortable: false,
        editable: true,
        resizable: true,
        selectable: true,
        scrollable: false,
        columns: this.get_Columnas(),
        scrollable: true,
        pageable: true,
        noRecords: {
            template: "<div class='grid-empy'> No se encontraron registros </div>"
        },  
        dataBound: this.set_Icons,      
    }
}
GridPrincipal.prototype.get_Config_Disable = function () {

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
        pageable: true,
        noRecords: {
            template: "<div class='grid-empy'> No se encontraron registros </div>"
        },  
        dataBound: this.set_Icons,      
    }
}
GridPrincipal.prototype.get_Campos = function (e) {

    return {
        pk: { type: "string", editable: false },
        articulo: { type: "string", editable: false },
        cabecera: { type: "string", editable: false },
        articulo_clave: { type: "string", editable: false },
        cantidad: { type: "number" },   
        articulo_udm: { type: "string", editable: false },
    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { field: "articulo_clave" , title: "Articulo"},
        { field: "cantidad" , title: "Cantidad"},
        { field: "articulo_udm", title: "Unidad de Medida"},
        {
           command: [ 
                {
                   text: " Eliminar",
                   click: this.click_BotonEliminar,
                   className: "boton_eliminar fa fa-trash-o"
                },  
                {
                   text: " Stock",
                   click: this.click_BotonStock,
                   className: "boton_default fa fa-th-large"
                }, 
            ],           
           title: " ",
           width: "200px"
        },
    ]
}
GridPrincipal.prototype.click_BotonEliminar = function (e) {

    e.preventDefault()

    if (targeta_filtros.$estado.val() == "CERRADO") {

        console.log(targeta_filtros.$estado.val())
        alertify.error("No se puede eliminar detalle de un movimiento cerrado")
    }
    else {
        var fila = this.dataItem($(e.currentTarget).closest('tr'))
    
        alertify.confirm(
            'Eliminar Registro',
            '¿Desea eliminar esta fila?', 

            function () {

                var url = url_grid + fila.pk + "/"

                $.ajax({
                    url: url,
                    method: "DELETE",
                    success: function () {
                        alertify.success("Se eliminó registro correctamente")

                        targeta_resultados.grid.kfuente_datos.remove(fila)
                        
                    },
                    error: function () {
                        
                        alertify.error("Ocurrió un error al eliminar")
                    }
                })
            }, 
            null
        )

    }
    
}
GridPrincipal.prototype.click_BotonStock = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_stock + targeta_filtros.$almacen_origen.val() + "/" + fila.articulo + "/"
}
GridPrincipal.prototype.set_Icons = function (e) {

    e.sender.tbody.find(".k-button.fa.fa-trash-o").each(function(idx, element){
        $(element).removeClass("fa fa-trash-o").find("span").addClass("fa fa-trash-o")
    })
    e.sender.tbody.find(".k-button.fa.fa-th-large").each(function(idx, element){
        $(element).removeClass("fa fa-th-large").find("span").addClass("fa fa-th-large")
    }) 
    
}
GridPrincipal.prototype.get_FuenteDatosConfig = function (e) {

    return {

        serverPaging: true,
        pageSize: 10,
        transport: {
            read: {

                url: url_grid,
                type: "GET",
                dataType: "json",
            },
            parameterMap: function (data, action) {
                if (action === "read") {

                    return targeta_filtros.get_Filtros(data.page, data.pageSize)
                }
            }
        },
        schema: {
            data: "results",
            total: "count",
            model: {
                fields: this.get_Campos()
            }
        },
        change: function (e) {

            if (e.action == "itemchange" && e.field == "cantidad") {

                var id = e.items[0].pk
                var articulo = e.items[0].articulo
                var cabecera = e.items[0].cabecera
                var cantidad = e.items[0].cantidad

               targeta_resultados.grid.cambiar_CantidadLinea(id, articulo, cabecera, cantidad)

            }
        },        
        error: function (e) {
            alertify.error("Status: " + e.status + "; Error message: " + e.errorThrown)
        },
    }
}
GridPrincipal.prototype.get_FuenteDatosConfigExcel = function (e) {

    return {
        
        transport: {
            read: {

                url: url_detalle_excel,
                type: "GET",
                dataType: "json",
            },
            parameterMap: function (data, action) {
                if (action === "read") {

                    return targeta_filtros.get_Filtros()
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
GridPrincipal.prototype.buscar =  function() {
    this.kfuente_datos.page(1)
}
GridPrincipal.prototype.ocultar_Botones = function () {

    var grid = this.kgrid.data("kendoGrid")
    grid.hideColumn(3)
}
GridPrincipal.prototype.cambiar_CantidadLinea = function (_id, _articulo, _cabecera, _cantidad) {

    var url_update = url_grid + _id + "/"
    var url_article = url_articulos_upd.replace("articulo_id", _articulo)
    var url_header = url_cabecera_upd.replace("cabecera_id", _cabecera)

    data = {
        'articulo': _articulo, 
        'cabecera': _cabecera,
        'cantidad': _cantidad,
    }

    $.ajax({

        url: url_update,
        data : JSON.stringify(data),
        dataType: "json",
        type: "PUT",
        contentType: "application/json; charset=utf-8",

        success: function (e) {
            alertify.warning("Se actualizo cantidad")
        },
        error: function (e) {
            alertify.error(e.mensaje)
        }
    })    

}


/*-----------------------------------------------*\
            OBJETO: TOOLBAR
\*-----------------------------------------------*/

function Toolbar() {
    this.$boton_nuevo = $('#boton_nuevo')
    this.$boton_exportar = $("#boton_exportar")

    this.init()
}
Toolbar.prototype.init = function (e) {
    this.$boton_nuevo.on("click", this, this.click_BotonNuevo)
    this.$boton_exportar.on("click", this, this.click_BotonExportar)
}

Toolbar.prototype.Inicializar_CeldasExcel = function (e) {

    if (targeta_resultados.grid.get_Columnas != null)
    {
        if (targeta_resultados.grid.get_Columnas.length != 1) {
            targeta_resultados.grid.get_Columnas.length = 0;
        }
    }

    this.kRows = [{
        cells: [
            { value: 'Articulo'},
            { value: 'Cantidad' },
            { value: 'UDM' },
        ]
    }];
}
Toolbar.prototype.click_BotonExportar = function (e) {

    e.preventDefault();

    e.data.Inicializar_CeldasExcel();

    
        targeta_resultados.grid.kfuente_datos_excel.fetch(function () {

            var data = this.data();
            for (var i = 0; i < data.length; i++) {

                e.data.kRows.push({
                    cells: [
                        { value: data[i].articulo_clave },
                        { value: data[i].cantidad },
                        { value: data[i].articulo_udm },
                    ]
                })
            }
            var workbook = new kendo.ooxml.Workbook({
                sheets: [
                    {
                        columns: [
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                    
                        ],
                        title: "OT_Detalle",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "OrdenTrabajo_Detalle.xlsx",
            });
        });
}

Toolbar.prototype.click_BotonNuevo = function (e) {

    e.preventDefault()
    $('#modal_nuevo').modal('show');
}
Toolbar.prototype.deshabilitar_Campos = function () {
    this.$boton_nuevo.addClass("hidden", true)
    //this.$boton_exportar.attr("disabled", true)
}
/*-----------------------------------------------*\
            OBJETO: ModalDetalle
\*-----------------------------------------------*/

function ModalDetalle() {

    this.$id = $("#modal_nuevo")
    this.$cabecera = $('#cabecera')
    this.$articulo = $('#id_articulo')
    this.$cantidad = $('#id_cantidad')
    this.$boton_guardar = $('#boton_guardar_detalle')
    this.$articulo_contenedor = $('#articulo_contenedor')
    this.$articulo_mensaje = $('#articulo_mensaje')
    this.$cantidad_contenedor = $('#cantidad_contenedor')
    this.$cantidad_mensaje = $('#cantidad_mensaje')

    this.init()
}

ModalDetalle.prototype.init = function () {
    
    this.$articulo.select2()
    this.$boton_guardar.on("click", this, this.click_BotonGuardar)
    this.$id.on('show.bs.modal', this, this.load)
    this.load_articulos()
}
ModalDetalle.prototype.load = function (e) {

    e.data.clear_Estilos()
    e.data.clear_Fields()
}
ModalDetalle.prototype.clear_Estilos = function () {

    this.$articulo_contenedor.removeClass("has-error")

    if(this.$articulo_mensaje.hasClass('hidden') != null) { 
        this.$articulo_mensaje.addClass('hidden')
    } 

    this.$cantidad_contenedor.removeClass("has-error")  

    if(this.$cantidad_mensaje.hasClass('hidden') != null) { 
        this.$cantidad_mensaje.addClass('hidden')
    } 
}
ModalDetalle.prototype.clear_Fields = function () {

    this.$articulo.val("").trigger('change')
    this.$cantidad.val("")

    
}
ModalDetalle.prototype.load_articulos = function () {
    combo_articulos = this.$articulo
         $.ajax(
            {
                url: url_articulos,
                method: "GET",
                data: {
                "estado" :  "ACT"
            },
            success: function (response) {

            combo_articulos.append($('<option>', { 
                value: "",
                text : "-----------"
            }))            

            $.each(response, function (index, item) {
                if (item.clave == null){
                    clave = "-"
                }
                else{
                    clave = item.clave
                }
                 combo_articulos.append($('<option>', { 
                    value: item.pk,
                    text : item.informacion,
                    })
                )
            })
        },
        error: function (response) {
            
            alertify.error("Ocurrio error al consultar")
        }
    })
}
ModalDetalle.prototype.validar = function () {
    var bandera = true

    if ( this.$articulo.val() == "") {
        this.$articulo_contenedor.addClass("has-error")
        this.$articulo_mensaje.removeClass("hidden")
        bandera = false
    }

    if ( this.$cantidad.val() == "") {
        this.$cantidad_contenedor.addClass("has-error")
        this.$cantidad_mensaje.removeClass("hidden")
        bandera = false
    }

    return bandera
}

ModalDetalle.prototype.click_BotonGuardar = function (e) {

    if (e.data.validar()) {
        
        articulo = e.data.$articulo.val()
        cantidad = e.data.$cantidad.val()
        cabecera = e.data.$cabecera.val()

        var csrftoken = $("[name=csrfmiddlewaretoken]").val()

        $.ajax({
            headers: { "X-CSRFToken": csrftoken },
            url: url_grid,
            method: "POST",
            data: {
                "cantidad": cantidad,
                "articulo": articulo,
                "cabecera": cabecera,
            },
            success: function (){
                
                e.data.$id.modal('hide')

                alertify.success("Detalle Registrado")
                targeta_resultados.grid.kfuente_datos.read();

            },
            error: function(response){

                alertify.error("Error "+ response.status + " . No se guardó el registro")
                e.data.$id.modal('hide')

            }
           
                    
        });

    }
}