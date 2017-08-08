/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_grid = window.location.origin + "/api/movimientos/"
var url_excel = window.location.origin + "/api/movimientoexcel/"
var url_nuevo = window.location.origin + "/salidas/orden_trabajo/nuevo/"
var url_editar = window.location.origin + "/salidas/orden_trabajo/editar/"

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

    this.$descripcion = $('#id_descripcion')
    this.$fecha_inicio = $('#id_fecha_inicio')
    this.$fecha_fin = $('#id_fecha_fin')
    this.$almacen_origen = $('#id_almacen_origen')
    this.$orden_trabajo = $('#id_orden_trabajo')
    this.$persona_recibe = $('#id_persona_recibe')
    this.$persona_entrega = $('#id_persona_entrega')
    this.$estado = $('#id_estado')
    this.$tipo = $('#id_tipo')
    this.$boton_buscar =  $('#boton_buscar')
    this.$boton_limpiar =  $('#boton_limpiar')

    this.init()
}
TargetaFiltros.prototype.init = function () {

    this.$almacen_origen.select2()
    this.$persona_recibe.select2()
    this.$orden_trabajo.select2()
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
    
    tipo = "SAL"
    clasificacion = "OT"
    return {
        page: _page,
        pageSize: _pageSize,
        descripcion: this.$descripcion.val(),
        fecha_inicio: this.$fecha_inicio.val(),
        fecha_fin: this.$fecha_fin.val(),
        almacen_origen: this.$almacen_origen.val(),
        orden_trabajo: this.$orden_trabajo.val(),
        persona_recibe: this.$persona_recibe.val(),
        persona_entrega: this.$persona_entrega.val(),
        estado: this.$estado.val(),
        tipo: tipo,
        clasificacion: clasificacion,

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
    e.data.$almacen_origen.val("").trigger('change')
    e.data.$orden_trabajo.val("").trigger('change')
    e.data.$persona_recibe.val("")
    e.data.$persona_entrega.val("")
    e.data.$estado.val().trigger('change')

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
        pk : { type: "number" },
        fecha: { type: "date" },
        descripcion: { type: "string" },
        almacen_origen: { type: "string" },
        persona_recibe: { type: "string" },
        persona_entrega: { type: "string" },
    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { field: "pk" , title: "Clave", width: "80px" },
        { field: "fecha" , title: "Fecha", width: "100px", format: "{0:dd-MMMM-yyyy}" },
        { field: "descripcion" , title: "Descripción", width: "250px" },
        { field: "almacen_origen" , title: "Almacén Origen", width: "350px" },
        { field: "persona_entrega" , title: "Persona Entrega", width: "120px" },
        { field: "persona_recibe" , title: "Persona Recibe", width: "120px" },
        { field: "orden_trabajo" , title: "Orden de Trabajo", width: "170px" },
        { field: "estado" , title: "Estado", width: "120px" },
        { field: "created_by" , title: "Usuario", width: "120px" },

        {
           command: [
                {
                   text: " Editar",
                   click: this.click_BotonEditar,
                   className: "boton_editar fa fa-pencil"
                }, 
                
                             
            ],           
           title: " ",
           width: "170px"
        },
    ]
}
GridPrincipal.prototype.apply_Estilos = function (e) {

    // Aplicar Iconos
    e.sender.tbody.find(".k-button.fa.fa-pencil").each(function(idx, element){
        $(element).removeClass("fa fa-pencil").find("span").addClass("fa fa-pencil")
    })     
    // Aplicar formato a columna:
    $('td').each( function () {
        if($(this).text()=='CAPTURA'){ 
            $(this).addClass('cell--activo')
        }
        else if($(this).text()=='CERRADO'){ 
            $(this).addClass('cell--deshabilitado')
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

GridPrincipal.prototype.click_BotonEditar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_editar + fila.pk + "/"
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
            { value: 'Id Mov'},
            { value: 'Fecha' },
            { value: 'Descripcion' },
            { value: 'Almacen Origen' },
            { value: 'Persona Entrega' },
            { value: 'Persona Recibe' },
            { value: 'Orden de Trabajo' },
            { value: 'Estado' },
            { value: 'Creado Por' },
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
                        { value: data[i].fecha },
                        { value: data[i].descripcion },
                        { value: data[i].almacen_origen },
                        { value: data[i].persona_entrega },
                        { value: data[i].persona_recibe },
                        { value: data[i].orden_trabajo },
                        { value: data[i].estado },
                        { value: data[i].created_by },
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
                        title: "Ordenes de Trabajo",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "Salidas_OT.xlsx",
            });
        });
}