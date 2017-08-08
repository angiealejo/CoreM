/*-----------------------------------------------*\
            GLOBAL VARS
\*-----------------------------------------------*/

// URLS
var url_grid = window.location.origin + "/api/udmarticulo/"
var url_nuevo = window.location.origin + "/udmarticulo/nuevo/"
var url_editar = window.location.origin + "/udmarticulo/editar/"
var url_eliminar = window.location.origin + "/api/udmarticulo/"

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
            OBJETO: FILTROS
\*-----------------------------------------------*/

function TargetaFiltros() {

    this.$id = $('#id_panel')

    this.$filtro = $('#filtro');
    this.$boton_buscar =  $('#boton_buscar');
    
    this.init()
}
TargetaFiltros.prototype.init = function () {

    // this.$id.addClass('collapsed-box')

    this.$boton_buscar.on("click", this, this.click_BotonBuscar)
}
TargetaFiltros.prototype.click_BotonBuscar = function(e) {

    e.preventDefault()
    targeta_resultados.grid.buscar()
}
TargetaFiltros.prototype.get_Filtros = function () {

    return {
        search: this.$filtro.val()
        
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
        noRecords: {
            template: "<div class='grid-empy'> No se encontraron registros </div>"
        },
        dataBound: this.set_Icons,
    }
}
GridPrincipal.prototype.get_Campos = function (e) {

    return {
        clave: { type: "string"},
        descripcion: { type: "string" },
    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [      
        { field: "clave" , title: "Clave" },
        { field: "descripcion" , title: "Descripcion"},
        {
           command: [
                {
                   text: " Editar",
                   click: this.click_BotonEditar,
                   className: "boton_editar fa fa-pencil"
                },
                {
                    text: " Eliminar",
                    click: this.click_BotonEliminar,
                    className: "boton_eliminar fa fa-trash-o"
                },
            ],
           title: " ",
           width: "190px"
        },
    ]
}
GridPrincipal.prototype.set_Icons = function (e) {

    e.sender.tbody.find(".k-button.fa.fa-pencil").each(function(idx, element){
        $(element).removeClass("fa fa-pencil").find("span").addClass("fa fa-pencil")
    })

    e.sender.tbody.find(".k-button.fa.fa-trash-o").each(function(idx, element){
        $(element).removeClass("fa fa-trash-o").find("span").addClass("fa fa-trash-o")
    })
}
GridPrincipal.prototype.get_FuenteDatosConfig = function (e) {

    return {
        transport: {
            read: {

                url: url_grid,
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
    
    this.kfuente_datos.read()
}
GridPrincipal.prototype.click_BotonEditar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_editar + fila.pk;
}
GridPrincipal.prototype.click_BotonEliminar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))

    alertify.confirm(
        'Eliminar Registro',
        '¿Desea Eliminar este registro?', 
        function () {

            var url = url_eliminar + fila.pk + "/"

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
    this.$boton_exportar = $("#boton_exportar")

    this.init()
}
Toolbar.prototype.init = function (e) {

    this.$boton_nuevo.on("click", this, this.click_BotonNuevo)
    this.$boton_exportar.on("click", this, this.click_BotonExportar)
}
Toolbar.prototype.click_BotonNuevo = function (e) {

    e.preventDefault()
    window.location.href = url_nuevo
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
            { value: 'Tag' },
            { value: 'Descripcion' },     
        ]
    }];
}
Toolbar.prototype.click_BotonExportar = function (e) {

    e.preventDefault();

    e.data.Inicializar_CeldasExcel();

    
        targeta_resultados.grid.kfuente_datos.fetch(function () {

            var data = this.data();
            for (var i = 0; i < data.length; i++) {

                e.data.kRows.push({
                    cells: [
                        { value: data[i].pk },
                        { value: data[i].clave },
                        { value: data[i].descripcion },
                        
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
                        title: "UDM Articulos",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "UDM_Articulos.xlsx",
            });
        });
}


