/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_grid = window.location.origin + "/api/ordenestrabajo/"
var url_excel = window.location.origin + "/api/ordenestrabajoexcel/"
var url_nuevo = window.location.origin + "/ordenes/nuevo/"
var url_editar = window.location.origin + "/ordenes/editar/"
var url_anexos = window.location.origin + "/ordenes/anexos/"
var url_imprimir = window.location.origin + "/ordenes/preview/"
var url_reporte = window.location.origin + "/ordenes/reporte/preview/"

var current_url = window.location.pathname


// OBJS
var targeta_filtros = null
var targeta_resultados = null


/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    this.$id = $('#id_filtros')

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
    this.$numero_orden = $('#id_numero_orden')
    this.$equipo = $('#id_equipo')
    this.$descripcion = $('#id_descripcion')
    this.$especialidad = $('#id_especialidad')
    this.$tipo = $('#id_tipo')
    this.$estado = $('#id_estado')
    this.$responsable = $('#id_responsable')
    this.$solicitante = $('#id_solicitante')
    this.$fecha_inicio = $('#id_fecha_inicio')
    this.$fecha_fin = $('#id_fecha_fin')

    this.$boton_buscar =  $('#boton_buscar')
    this.$boton_limpiar =  $('#boton_limpiar')

    this.init()
}
TargetaFiltros.prototype.init = function () {
    
    this.$equipo.select2()
    this.$tipo.select2()
    this.$estado.select2()
    this.$responsable.select2()
    this.$solicitante.select2()
    this.$fecha_inicio.datepicker(this.get_DateConfig())
    this.$fecha_fin.datepicker(this.get_DateConfig())
    this.$id.addClass('collapsed-box')

    this.$boton_buscar.on("click", this, this.click_BotonBuscar)
    this.$boton_limpiar.on("click", this, this.click_BotonLimpiar)
}
TargetaFiltros.prototype.get_DateConfig = function () {
    return {
        autoclose: true,
        language: 'es',
        todayHighlight: true,
        clearBtn: true,
        todayBtn: true,
        startDate: '2017-01-01',
    }
}
TargetaFiltros.prototype.get_Filtros = function (_page, _pageSize) {
    // if (current_url == "/ordenes/terminadas/"){
    //     estado = "TER"
    // }
    // else if (current_url == "/ordenes/abiertas/"){
    //     estado = "CAP"
    // }
    // else {
    //     estado = this.$estado.val()
    // }
    return {
        page: _page,
        pageSize: _pageSize,
        id: this.$numero_orden.val(),
        equipo: this.$equipo.val(), 
        descripcion: this.$descripcion.val(),
        especialidad: this.$especialidad.val(),
        tipo: this.$tipo.val(),
        estado: this.$estado.val(),
        responsable: this.$responsable.val(),
        solicitante: this.$solicitante.val(),
        created_date_mayorque: this.$fecha_inicio.val(),
        created_date_menorque: this.$fecha_fin.val(),
    }
}
TargetaFiltros.prototype.get_FiltrosExcel = function () {

    return {
        id: this.$numero_orden.val(),
        equipo: this.$equipo.val(), 
        descripcion: this.$descripcion.val(),
        especialidad: this.$especialidad.val(),
        tipo: this.$tipo.val(),
        estado: this.$estado.val(),
        responsable: this.$responsable.val(),
        solicitante: this.$solicitante.val(),
        created_date_mayorque: this.$fecha_inicio.val(),
        created_date_menorque: this.$fecha_fin.val(),
    }
}
TargetaFiltros.prototype.click_BotonBuscar = function(e) {

    e.preventDefault()
    targeta_resultados.grid.buscar()
}
TargetaFiltros.prototype.click_BotonLimpiar = function (e) {

    e.preventDefault()
    e.data.$numero_orden.val("")
    e.data.$equipo.val("").trigger('change')
    e.data.$descripcion.val("")
    e.data.$especialidad.val("")
    e.data.$tipo.val("").trigger('change')
    e.data.$estado.val("").trigger('change')
    e.data.$responsable.val("").trigger('change')
    e.data.$solicitante.val("").trigger('change')
    e.data.$fecha_inicio.val("")
    e.data.$fecha_fin.val("")

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
        sortable: {
            mode: "multiple",
            allowUnsort: true
        },
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
        dataBound: this.apply_Estilos
    }

}
GridPrincipal.prototype.get_Campos = function (e) {

    return {
        pk: { type: "number" },
        equipo: { type: "string" },
        descripcion: { type: "string" },
        codigo_reporte: { type: "string" },
        especialidad: { type: "string" },
        tipo: { type: "string" },
        estado: { type: "string" },
        responsable: { type: "string" },
        solicitante: { type: "string" },
        fecha_estimada_inicio: { type: "date" },
        fecha_estimada_fin: { type: "date" },
        fecha_real_inicio: { type: "date" },
        fecha_real_fin: { type: "date" },
        created_date: { type: "date" },
    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [

        { field: "pk", title: "Numero", locked: true, width: "90px" },
        { field: "equipo", title: "Equipo", width: "350px" },
        { field: "descripcion", title: "Descripcion", width: "250px" },
        { field: "especialidad", title: "Especialidad", width: "200px" },
        { field: "tipo", title: "Tipo", width: "120px" },
        { field: "estado", title: "Estado", width: "120px" },
        { field: "responsable", title: "Responsable", width: "120px" },
        { field: "solicitante", title: "Solicitante", width: "120px" },
        { field: "fecha_estimada_inicio", title: "Fecha Estimada Inicio", width: "140px", format: "{0:dd-MMMM-yyyy}" },
        { field: "fecha_estimada_fin", title: "Fecha Estimada Fin", width: "140px", format: "{0:dd-MMMM-yyyy}" },
        { field: "fecha_real_inicio", title: "Fecha Real Inicio", width: "120px", format: "{0:dd-MMMM-yyyy}" },
        { field: "fecha_real_fin", title: "Fecha Real Fin", width: "120px", format: "{0:dd-MMMM-yyyy}" },
        { field: "codigo_reporte", title: "Código de Reporte", width: "120px" },
        { field: "created_date", title: "Fecha Creacion", width: "140px", format: "{0:dd-MMMM-yyyy}" },
        {
           command: [
                {
                   text: " Editar",
                   click: this.click_BotonEditar,
                   className: "boton_editar fa fa-pencil"
                },
                {
                    text: " Anexos",
                    click: this.click_BotonAnexos,
                    className: "boton_default fa fa-paperclip"
                },
                {
                   text: " Imprimir OT",
                   click: this.click_BotonImprimirOT,
                   className: "boton_default fa fa-wrench"
                },
                {
                    text: " Reporte Mantenimiento",
                    click: this.click_ReporteMantenimiento,
                    className: "boton_default fa fa-gear"
                },                            
            ],           
           title: " ",
           width: "490px"
        },
    ]
}
GridPrincipal.prototype.apply_Estilos = function (e) {

    // Aplicar iconos
    e.sender.tbody.find(".k-button.fa.fa-pencil").each(function(idx, element){
        $(element).removeClass("fa fa-pencil").find("span").addClass("fa fa-pencil")
    })

    e.sender.tbody.find(".k-button.fa.fa-paperclip").each(function(idx, element){
        $(element).removeClass("fa fa-paperclip").find("span").addClass("fa fa-paperclip")
    }) 

    // Aplicar iconos
    e.sender.tbody.find(".k-button.fa.fa-wrench").each(function(idx, element){
        $(element).removeClass("fa fa-wrench").find("span").addClass("fa fa-wrench")
    })

    e.sender.tbody.find(".k-button.fa.fa-gear").each(function(idx, element){
        $(element).removeClass("fa fa-gear").find("span").addClass("fa fa-gear")
    })           

    // Aplicar formato a columna:
    $('td').each( function () {
        if($(this).text()=='ABIERTA'){ 
            $(this).addClass('cell--activo')
        }
        else if($(this).text()=='CERRADA'){ 
            $(this).addClass('cell--deshabilitado')
        }
        else if($(this).text()=='CANCELADA'){ 
            $(this).addClass('cell--red')
        }        
        else if($(this).text()=='TERMINADA'){ 
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

                    return targeta_filtros.get_FiltrosExcel()
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
GridPrincipal.prototype.leer_Datos = function() {
    
    this.kfuente_datos_excel.read()
}
GridPrincipal.prototype.click_BotonEditar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_editar + fila.pk + "/"
}
GridPrincipal.prototype.click_BotonAnexos = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_anexos + fila.pk + "/texto/"
}
GridPrincipal.prototype.click_BotonImprimirOT = function (e) {
    
    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_imprimir + fila.pk +"/"
    //Abrir en una nueva pestaña
    //var win = window.open(url_imprimir+fila.pk, '_blank')
    //win.focus()
}
GridPrincipal.prototype.click_ReporteMantenimiento = function (e) {
    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_reporte + fila.pk +"/"
    //Abrir en una nueva pestaña
    //var win = window.open(url_reporte+fila.pk, '_blank')
    //win.focus()
}
GridPrincipal.prototype.change_IsTemplate = function (_value) {

    if (_value == "True") {
        return "SI"    
    }
    else {
        return "NO"
    }
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
            { value: 'Equipo' },
            { value: 'Descripcion' },
            { value: 'Especialidad' },
            { value: 'Tipo' },
            { value: 'Estado' },
            { value: 'Responsable' },
            { value: 'Fecha Estimada de Inicio' },
            { value: 'Fecha Estimada de Fin' },
            { value: 'Fecha Real de Inicio' },
            { value: 'Fecha Real de Fin' },
            { value: 'Codigo Reporte' },
            { value: 'Es Template' },
            { value: 'Fecha Creacion' },
        ]
    }];
}
Toolbar.prototype.click_BotonExportar = function (e) {


    targeta_resultados.grid.leer_Datos()
    e.data.Inicializar_CeldasExcel()

    targeta_resultados.grid.kfuente_datos_excel.fetch(function () {

        var data = this.data();
        for (var i = 0; i < data.length; i++) {

            e.data.kRows.push({
                cells: [
                    { value: data[i].pk },
                    { value: data[i].equipo },
                    { value: data[i].descripcion },
                    { value: data[i].especialidad },
                    { value: data[i].tipo },
                    { value: data[i].estado },
                    { value: data[i].responsable },
                    { value: data[i].fecha_estimada_inicio },
                    { value: data[i].fecha_estimada_fin },
                    { value: data[i].fecha_real_inicio },
                    { value: data[i].fecha_real_fin },
                    { value: data[i].codigo_reporte },
                    { value: data[i].es_template },
                    { value: data[i].created_date },
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
                    title: "Ordenes de Trabajo",
                    rows: e.data.kRows
                }
            ]
        });
        kendo.saveAs({
            dataURI: workbook.toDataURL(),
            fileName: "OT.xlsx",
        });
    });
}