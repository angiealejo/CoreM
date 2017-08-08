/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_grid = window.location.origin + "/api/solicitudescompradetalles/"
var url_excel = window.location.origin + "/api/solicitudescompradetalleexcel/"
var url_editar = window.location.origin + "/solicitudes_compra/editar/"
var url_articulos = window.location.origin + "/api/articulos2/"
var url_almacenes = window.location.origin + "/api/almacenes/"
var url_almacenes2 = window.location.origin + "/api/almacenes2/"

// OBJS
var targeta_filtros = null
var targeta_resultados = null
var modal_detalle = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    targeta_filtros = new TargetaFormulario()
    //console.log(targeta_filtros.$cabecera.val())
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

    this.$cabecera = $('#id_cabecera')
    this.$estado = $('#id_estado')
    this.$descripcion = $('#id_descripcion')
    this.$comentarios = $('#id_comentarios')
    this.$solicitante = $('#id_solicitante')
    this.$boton_guardar = $('#boton_guardar')
    this.init()
}
TargetaFormulario.prototype.init = function () {
    this.$comentarios.wysihtml5({
        toolbar: {
            "font-styles": true,
            "emphasis": true,
            "lists": true,
            "html": false,
            "link": false,
            "image": false,
            "color": false,
            "blockquote": false,
        }
    })
    this.$solicitante.select2()

}
TargetaFormulario.prototype.deshabilitar_Campos = function () {
    
        this.$descripcion.attr("disabled", true)
        this.$solicitante.attr("disabled", true)
        this.$boton_guardar.attr("disabled", true)

}
TargetaFormulario.prototype.get_Filtros = function (_page, _pageSize) {

    return {
        page: _page,
        pageSize: _pageSize,
        encabezado: this.$cabecera.val(),

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
    this.$boton_finalizar = $('#boton_finalizar')
    this.kfuente_datos = null
    this.kgrid = null

    this.init()
}
GridPrincipal.prototype.init = function () {

    kendo.culture("es-MX")
    this.kfuente_datos = new kendo.data.DataSource(this.get_FuenteDatosConfig())
    this.kfuente_datos_excel = new kendo.data.DataSource(this.get_FuenteDatosExcelConfig())

    this.kGrid = this.$id.kendoGrid(this.get_Config())

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
        pageable: true,
        noRecords: {
            template: "<div class='grid-empy'> No se encontraron registros </div>"
        },  
        dataBound: this.set_Icons,      
    }
}
GridPrincipal.prototype.get_Campos = function (e) {

    return {
        articulo_clave: { type: "string" },
        cantidad: { type: "string" },
        articulo_udm: { type: "string"},
        comentarios: { type: "string"},
        
    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { field: "articulo_clave" , title: "Articulo"},
        { field: "cantidad" , title: "Cantidad"},
        { field: "articulo_udm", title: "Unidad de Medida"},
        { field: "comentarios", title: "Comentarios", format: '{0:n2}', encoded: false},
        
        {
           command: [ 
                {
                   text: " Eliminar",
                   click: this.click_BotonEliminar,
                   className: "boton_eliminar fa fa-trash-o"
                },   
                             
            ],           
           title: " ",
           width: "120px"
        },
    ]
}
GridPrincipal.prototype.click_BotonEliminar = function (e) {
    e.preventDefault()
    if (targeta_filtros.$estado.val() == "CER") {
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
GridPrincipal.prototype.set_Icons = function (e) {

    e.sender.tbody.find(".k-button.fa.fa-trash-o").each(function(idx, element){
        $(element).removeClass("fa fa-trash-o").find("span").addClass("fa fa-trash-o")
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
        error: function (e) {
            alertify.error("Status: " + e.status + "; Error message: " + e.errorThrown)
        },
    }
}
GridPrincipal.prototype.get_FuenteDatosExcelConfig = function (e) {

    return {

        transport: {
            read: {

                url: url_excel,
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
    this.leer_Datos()
}
GridPrincipal.prototype.leer_Datos = function() {
    
    this.kfuente_datos_excel.read()
}
GridPrincipal.prototype.click_BotonEditar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_editar + fila.pk + "/"
}
GridPrincipal.prototype.ocultar_Botones = function () {

    var grid = this.kGrid.data("kendoGrid")
    grid.hideColumn(4)
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
Toolbar.prototype.deshabilitar_Campos = function () {
    this.$boton_nuevo.attr("disabled", true)
    //this.$boton_exportar.attr("disabled", true)
}
Toolbar.prototype.click_BotonNuevo = function (e) {

    e.preventDefault()
    $('#modal_nuevo').modal('show');
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
            { value: 'Unidad de Medida' },
            { value: 'Comentarios' },
            
        ]
    }];
}
Toolbar.prototype.click_BotonExportar = function (e) {

    //targeta_resultados.grid.leer_Datos()
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
                        { value: data[i].comentarios },
                        
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
                            { autoWidth: true },
                    
                        ],
                        title: "Solicitud de Compra",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "Solicitud_Compra.xlsx",
            });
        });
}

/*-----------------------------------------------*\
            OBJETO: ModalDetalle
\*-----------------------------------------------*/

function ModalDetalle() {

    this.$id = $("#modal_nuevo")
    this.$cabecera = $('#id_cabecera')
    this.$articulo = $('#id_articulo')
    this.$cantidad = $('#id_cantidad')
    this.$boton_guardar = $('#boton_guardar_detalle')
    this.$articulo_contenedor = $('#articulo_contenedor')
    this.$articulo_mensaje = $('#articulo_mensaje')
    this.$cantidad_contenedor = $('#cantidad_contenedor')
    this.$cantidad_mensaje = $('#cantidad_mensaje')
    this.$comentarios = $('#id_comentarios_modal')

    this.init()    
    
}

ModalDetalle.prototype.init = function () {
    
    this.$articulo.select2()
    this.$comentarios.wysihtml5({
        toolbar: {
            "font-styles": true,
            "emphasis": true,
            "lists": true,
            "html": false,
            "link": false,
            "image": false,
            "color": false,
            "blockquote": false,
        }
    })
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
                if (item.clave == null ){
                    clave = "-"
                }
                else {
                    clave = item.clave
                }
                 combo_articulos.append($('<option>', { 
                    value: item.pk,
                    text : "(clave) descripcion (udm)".replace("clave", clave).replace("descripcion", item.descripcion).replace("udm", item.udm)
                }))
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
        
        cantidad = e.data.$cantidad.val()
        articulo = e.data.$articulo.val()
        comentarios = e.data.$comentarios.val()
        cabecera = e.data.$cabecera.val()
        //console.log(cantidad)
        //console.log(articulo)
        //console.log(cabecera)
        $.ajax({

            url: url_grid,
            method: "POST",
            data: {
                "cantidad": cantidad,
                "articulo": articulo,
                "comentarios": comentarios,
                "encabezado": cabecera,
            },
            success: function (){
                //console.log(modal_detalle)
                modal_detalle.$id.modal('hide')

                alertify.success("Detalle Registrado")
                targeta_resultados.grid.kfuente_datos.read();
                //targeta_resultados.grid.$boton_finalizar.attr("disabled", false)


            },
            error: function(e){

                alertify.error("Error "+ e.status + " . No se guardó el registro")
                //console.log(modal_detalle)
                modal_detalle.$id.modal('hide')

            }
           
                    
        });

    }
}