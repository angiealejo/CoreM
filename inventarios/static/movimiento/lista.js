/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_grid = window.location.origin + "/api/inventario/"
var url_excel = window.location.origin + "/api/inventarioexcel/"
var url_nuevo = window.location.origin + "/entradas/compras/nuevo/"
var url_detalle = window.location.origin + "/movimientos/detalle/"
var url_ent_saldo_inicial = window.location.origin + "/entradas/saldo_inicial/editar/"
var url_ent_compras = window.location.origin + "/entradas/compras/editar/"
var url_ent_ajustes = window.location.origin + "/entradas/ajustes/editar/"
var url_ent_traspaso = window.location.origin + "/entradas/traspaso/ver/"

var url_sal_personal = window.location.origin + "/salidas/personal/editar/"
var url_sal_ot = "/salidas/orden_trabajo/editar/"
var url_sal_ajustes = "/salidas/ajustes/editar/"
var url_sal_traspaso = "/salidas/traspaso/editar/"
// OBJS
var targeta_filtros = null
var targeta_resultados = null
var pagina = null


/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    targeta_filtros = new TargetaFiltros()
    targeta_resultados = new TargetaResultados()

    pagina = new Pagina()
    pagina.init_Alertify()    
})

// Asigna eventos a teclas
$(document).keypress(function (e) {

    // Tecla Enter
    if (e.which == 13) {

        targeta_resultados.grid.buscar()
    }
})


/*-----------------------------------------------*\
            OBJETO: Targeta Filtros
\*-----------------------------------------------*/

function TargetaFiltros() {

    this.$id = $('#id_panel')

    this.$descripcion = $('#id_descripcion_encabezado')
    this.$fecha_inicio = $('#id_fecha_inicio')
    this.$fecha_fin = $('#id_fecha_fin')
    this.$almacen_destino = $('#id_almacen_destino')
    this.$almacen_origen = $('#id_almacen_origen')
    this.$persona_recibe = $('#id_persona_recibe')
    this.$persona_entrega = $('#id_persona_entrega')
    this.$proveedor = $('#id_proveedor')
    this.$estado = $('#id_estado')
    this.$tipo = $('#id_tipo')
    this.$articulo = $('#id_articulo')
    this.$clasificacion = $('#id_clasificacion')
    this.$boton_buscar =  $('#boton_buscar')
    this.$boton_limpiar =  $('#boton_limpiar')

    this.init()
}
TargetaFiltros.prototype.init = function () {
    this.$persona_recibe.select2()
    this.$persona_entrega.select2()
    this.$almacen_destino.select2()
    this.$almacen_origen.select2()
    this.$articulo.select2()
    this.$fecha_inicio.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha_inicio.datepicker(this.get_DateConfig())
    this.$fecha_fin.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha_fin.datepicker(this.get_DateConfig())
    this.$id.addClass('collapsed-box')

    this.$boton_buscar.on("click", this, this.click_BotonBuscar)
    this.$boton_limpiar.on("click", this, this.click_BotonLimpiar)
}
TargetaFiltros.prototype.get_DateConfig = function (){

    return {
        autoclose: true,
        language: 'es',
        todayHighlight: true,
        clearBtn: true,
        startDate: '2017-01-01',
    }
}
TargetaFiltros.prototype.get_Filtros = function (_page, _pageSize) {
    
    return {
        page: _page,
        pageSize: _pageSize,
        cabecera__descripcion: this.$descripcion.val(),
        fecha_inicio: this.$fecha_inicio.val(),
        fecha_fin: this.$fecha_fin.val(),
        cabecera__almacen_destino: this.$almacen_destino.val(),
        cabecera__almacen_origen: this.$almacen_origen.val(),
        cabecera__persona_recibe: this.$persona_recibe.val(),
        cabecera__persona_entrega: this.$persona_entrega.val(),
        cabecera__proveedor: this.$proveedor.val(),
        cabecera__estado: this.$estado.val(),
        cabecera__tipo: this.$tipo.val(),
        cabecera__clasificacion: this.$clasificacion.val(),
        articulo: this.$articulo.val(),

    }
}
TargetaFiltros.prototype.click_BotonBuscar = function(e) {

    e.preventDefault()
    targeta_resultados.grid.buscar()
}
TargetaFiltros.prototype.click_BotonLimpiar = function (e) {

    e.preventDefault()

    e.data.$descripcion.val("")
    e.data.$fecha_inicio.val("")
    e.data.$fecha_fin.val("")
    e.data.$almacen_destino.val("").trigger('change')
    e.data.$almacen_origen.val("").trigger('change')
    e.data.$persona_recibe.val("").trigger('change')
    e.data.$persona_entrega.val("").trigger('change')
    e.data.$proveedor.val("")
    e.data.$estado.val("").trigger('change')
    e.data.$tipo.val("").trigger('change')
    e.data.$clasificacion.val("").trigger('change')
    e.data.$articulo.val("").trigger('change')

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
    this.kfuente_datos_excel = null
    this.kgrid = null

    this.init()
}
GridPrincipal.prototype.init = function () {

    kendo.culture("es-MX")

    this.kfuente_datos = new kendo.data.DataSource(this.get_FuenteDatosConfig())
    this.kfuente_datos_excel = new kendo.data.DataSource(this.get_FuenteDatosExcel())

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
        scrollable: true,
        columns: this.get_Columnas(),
        scrollable: true,
        pageable: true,
        noRecords: {
            template: "<div class='grid-empy'> No se encontraron registros </div>"
        },  
        dataBound: this.apply_Estilos,      
    }
}
GridPrincipal.prototype.get_Campos = function (e) {

    return {
        pk: { type: "string" },
        cabecera_fecha: { type: "date" },
        articulo: { type: "string" },
        articulo_detalle: { type: "string" },
        cantidad: { type: "number" },
        cabecera: { type: "string" },
        cabecera_descripcion: { type: "string" },
        cabecera_clasificacion: { type: "string" },
        cabecera_estado: { type: "string" },
        cabecera_almacen_origen: { type: "string" },
        cabecera_almacen_destino: { type: "string" },
        cabecera_proveedor: { type: "string" },
        cabecera_persona_recibe: { type: "string" },
        cabecera_persona_entrega: { type: "string" },
        cabecera_created_by: { type: "string" },
    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { field: "cabecera_tipo" , title: "Tipo Movimiento", width: "100px" },
        { field: "cabecera_clasificacion" , title: "Clasif. Movimiento", width: "180px" },
        { field: "cabecera_fecha" , title: "Fecha", width: "100px", format: "{0:dd-MMMM-yyyy}" },
        { field: "articulo_detalle" , title: "Articulo", width: "200px" },
        { field: "cantidad" , title: "Cantidad", width: "100px" },
        { field: "articulo_udm" , title: "UDM", width: "100px" },
        { field: "cabecera_descripcion" , title: "Descripción Movimiento", width: "200px" },
        { field: "cabecera_estado" , title: "Estado Enc.", width: "120px" },
        { field: "cabecera_almacen_origen" , title: "Almacén Origen", width: "350px" },
        { field: "cabecera_almacen_destino" , title: "Almacén Destino", width: "350px" },
        { field: "cabecera_orden_trabajo" , title: "OT", width: "120px" },
        { field: "cabecera_proveedor" , title: "Proveedor", width: "150px" },
        { field: "cabecera_persona_recibe" , title: "Persona Recibe", width: "170px" },
        { field: "cabecera_persona_entrega" , title: "Persona Entrega", width: "170px" },
        { field: "cabecera_created_by" , title: "Creado por", width: "170px" },

        {
           command: [
                {
                   text: " Ver Documento",
                   click: this.click_BotonVerDetalle,
                   className: "boton_editar fa fa-file-text-o"
                }, 
                
                             
            ],           
           title: " ",
           width: "150px"
        },
    ]
}
GridPrincipal.prototype.click_BotonVerDetalle = function (e) {
    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    console.log(fila.cabecera_clasificacion)
    if (fila.cabecera_clasificacion == "SALDO INICIAL"){
        // window.open(url_ent_saldo_inicial + fila.cabecera + "/", '_blank')
        window.location.href = url_ent_saldo_inicial + fila.cabecera + "/"
    }
    else if (fila.cabecera_clasificacion == "COMPRA"){
        // window.open(url_ent_compras + fila.cabecera + "/", '_blank')
        window.location.href = url_ent_compras + fila.cabecera + "/"
    }
    else if(fila.cabecera_clasificacion == "AJUSTE" && fila.cabecera_tipo=="ENTRADA"){
        // window.open(url_ent_ajustes + fila.cabecera + "/", '_blank')
        window.location.href = url_ent_ajustes + fila.cabecera + "/"
    }
    else if(fila.cabecera_clasificacion == "TRASPASO" && fila.cabecera_tipo=="ENTRADA"){
        // window.open(url_ent_traspaso + fila.cabecera + "/", '_blank')
        window.location.href = url_ent_traspaso + fila.cabecera + "/"
    }
    else if(fila.cabecera_clasificacion == "DESPACHO A PERSONAL"){
        // window.open(url_sal_personal + fila.cabecera + "/", '_blank')
        window.location.href = url_sal_personal + fila.cabecera + "/"
    }
    else if(fila.cabecera_clasificacion == "ORDEN TRABAJO"){
        // window.open(url_sal_ot + fila.cabecera + "/", '_blank')
        window.location.href = url_sal_ot + fila.cabecera + "/"
    }
    else if(fila.cabecera_clasificacion == "AJUSTE" && fila.cabecera_tipo=="SALIDA"){
        // window.open(url_sal_ajustes + fila.cabecera + "/", '_blank')
        window.location.href = url_sal_ajustes + fila.cabecera + "/"
    }
    else if(fila.cabecera_clasificacion == "TRASPASO" && fila.cabecera_tipo=="SALIDA"){
        // window.open(url_sal_traspaso + fila.cabecera + "/", '_blank')
        window.location.href = url_sal_traspaso + fila.cabecera + "/"
    }
    

}
GridPrincipal.prototype.apply_Estilos = function (e) {

    // Aplicar Iconos
    e.sender.tbody.find(".k-button.fa.fa-file-text-o").each(function(idx, element){
        $(element).removeClass("fa fa-file-text-o").find("span").addClass("fa fa-file-text-o")
    })     
    // Aplicar formato a columna:
    $('td').each( function () {
        if($(this).text()=='CAPTURA'){ 
            $(this).addClass('cell--activo')
        }
        else if($(this).text()=='CERRADO'){ 
            $(this).addClass('cell--deshabilitado')
        }
        else if($(this).text()=='EN TRANSITO'){ 
            $(this).addClass('cell--terminada')
        }
    })

}
GridPrincipal.prototype.get_FuenteDatosExcel = function (e) {

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
GridPrincipal.prototype.buscar =  function() {
    this.kfuente_datos.page(1)
    this.kfuente_datos_excel.read()
}

/*-----------------------------------------------*\
            OBJETO: TOOLBAR
\*-----------------------------------------------*/

function Toolbar() {
   
    this.$boton_exportar = $("#boton_exportar")

    this.init()
}
Toolbar.prototype.init = function (e) {

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
            { value: 'Tipo'},
            { value: 'Clasificacion'},
            { value: 'Fecha'},
            { value: 'Articulo'},
            { value: 'Cantidad'},
            { value: 'Descripcion Encabezado'},
            { value: 'Estado Movimiento'},
            { value: 'Almacen Origen'},
            { value: 'Almacen Destino'},
            { value: 'Proveedor'},
            { value: 'cabecera_orden_trabajo'},
            { value: 'Persona Recibe'},
            { value: 'Persona Entrega'},
            { value: 'Creado Por'},

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
                        { value: data[i].cabecera_tipo },
                        { value: data[i].cabecera_clasificacion },
                        { value: data[i].cabecera_fecha },
                        { value: data[i].articulo_detalle },
                        { value: data[i].cantidad },
                        { value: data[i].cabecera_descripcion },
                        { value: data[i].cabecera_estado },
                        { value: data[i].cabecera_almacen_origen},
                        { value: data[i].cabecera_almacen_destino },
                        { value: data[i].cabecera_proveedor },
                        { value: data[i].cabecera_orden_trabajo },
                        { value: data[i].cabecera_persona_recibe },
                        { value: data[i].cabecera_persona_entrega },
                        { value: data[i].cabecera_created_by },
                       
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
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },
                            { autoWidth: true },                           
                    
                        ],
                        title: "Movimientos Almacen",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "Movimientos_Almacen.xlsx",
            });
        });
}