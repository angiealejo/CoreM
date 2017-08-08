/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

var url_grid = window.location.origin + "/api/stock/"
var url_excel = window.location.origin + "/api/stockexcel/"
var targeta_filtros = null
var targeta_resultados = null
var modal= null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    targeta_filtros = new TargetaFiltros()
    targeta_resultados = new TargetaResultados()
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

    this.$articulo = $('#id_articulo') 
    this.$almacen = $('#id_almacen') 
    this.$cantidad_mayorque = $('#id_cantidad_mayorque')
    this.$cantidad_menorque = $('#id_cantidad_menorque')

    this.$boton_buscar =  $('#boton_buscar')
    this.$boton_limpiar =  $('#boton_limpiar')

    this.init()
}
TargetaFiltros.prototype.init = function () {

    pagina.activar_Arbol("tree_inventarios")

    if (this.$articulo.val() != "") {
        alertify.warning("Existencias del articulo: " + this.$articulo.find(":selected").text())
        pagina.activar_Opcion("opt_articulos")
    }

    if (this.$almacen.val() != "") {
        alertify.warning("Existencias en el almacen: " + this.$almacen.find(":selected").text())
        pagina.activar_Opcion("opt_almacenes")
    }    

    this.$articulo.select2()
    this.$almacen.select2()

    this.$id.addClass('collapsed-box')

    this.$boton_buscar.on("click", this, this.click_BotonBuscar)
    this.$boton_limpiar.on("click", this, this.click_BotonLimpiar)
}
TargetaFiltros.prototype.get_Filtros = function (_page, _pageSize) {

    return {
        page: _page,
        pageSize: _pageSize,

        articulo: this.$articulo.val(),
        almacen: this.$almacen.val(),
        cantidad_mayorque: this.$cantidad_mayorque.val(),
        cantidad_menorque: this.$cantidad_menorque.val(),
        
    }
}
TargetaFiltros.prototype.click_BotonBuscar = function(e) {

    e.preventDefault()
    targeta_resultados.grid.buscar()
    
}
TargetaFiltros.prototype.click_BotonLimpiar = function (e) {

    e.preventDefault()
    e.data.$articulo.val("").trigger('change')
    e.data.$almacen.val("").trigger('change')
    e.data.$cantidad_mayorque.val("")
    e.data.$cantidad_menorque.val("")   
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

    this.kgrid = this.$id.kendoGrid(this.get_Config())
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
        dataBound: this.apply_Estilos,
    }
}
GridPrincipal.prototype.get_Campos = function (e) {

    return {
        almacen: { type: "string" },
        articulo: { type: "string" },
        udm: { type: "string"},
        cantidad: { type: "number"},
        articulo_stock_seg: { type: "number"},
        art_marca: { type: "string"},
        art_modelo: { type: "string"},
        art_numero_parte: { type: "string"},

    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { field: "almacen" , title: "Almacen", width: "120px" },
        { field: "articulo" , title: "Articulo", width: "120px" },
        { field: "udm" , title: "UDM", width: "120px" },
        { field: "art_marca" , title: "Marca", width: "120px" },
        { field: "art_modelo" , title: "Modelo", width: "120px" },
        { field: "art_numero_parte" , title: "No. Parte", width: "120px" },
        { field: "cantidad" , title: "Existencias", width: "120px", attributes: {
                    "class": "existencia"} },
        { field: "articulo_stock_seg" , title: "Stock de Seg.", width: "120px", attributes: {
                    "class": "stock-seg"}},
    ]
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
                cache: false

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
GridPrincipal.prototype.apply_Estilos = function (e) {
    
       $('tr').each(function(index, item){
            
        $this = $(this);

        var existencia = $this.closest("tr").find("td.existencia").text()
        var celda = $this.closest("tr").find("td.existencia")
        var stock = $this.closest("tr").find("td.stock-seg").text();
        e = parseInt(existencia)
        s = parseInt(stock)
        if (e > s) {
            celda.addClass("cell--green")
            //console.log("existencia > stock")

        }
        
        else if(e < s) {
            celda.addClass("cell--red")
            //console.log("existencia < stock")
        }

        else if(e == s ){
            celda.addClass("cell--yellow")
            //console.log("existencia == stock")
        }

    })

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
            { value: 'Id'},
            { value: 'Almacen' },
            { value: 'Clave'},
            { value: 'Articulo' },
            { value: 'UDM' },
            { value: 'Marca'},
            { value: 'Modelo'},
            { value: 'No. Parte'},
            { value: 'Existencias' },
            { value: 'Stock de Seguridad' },
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
                        { value: data[i].pk },
                        { value: data[i].almacen },
                        { value: data[i].articulo_clave },
                        { value: data[i].articulo },
                        { value: data[i].udm },
                        { value: data[i].art_marca },
                        { value: data[i].art_modelo },
                        { value: data[i].art_numero_parte},
                        { value: data[i].cantidad },
                        { value: data[i].articulo_stock_seg },
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
                        ],
                        title: "Stock",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "Stock.xlsx",
            });
        });
}