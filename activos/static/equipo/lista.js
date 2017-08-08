/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_grid = window.location.origin + "/api/equipos/"
var url_excel = window.location.origin + "/api/equipoexcel/"
var url_nuevo = window.location.origin + "/equipos/nuevo/"
var url_editar = window.location.origin + "/equipos/editar/"
var url_anexos = window.location.origin + "/equipos/anexos/"
var url_estructura = window.location.origin + "/equipos/arbol/"
var url_mediciones = window.location.origin + "/equipos/"
// OBJS
var targeta_filtros = null
var targeta_resultados = null

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

	this.$tag = $('#id_tag')
	this.$serie = $('#id_serie')
	this.$estado = $('#id_estado')
    this.$tipo = $('#id_tipo')
	this.$padre = $('#id_padre')
	this.$sistema = $('#id_sistema')
	this.$ubicacion = $('#id_ubicacion')
	this.$descripcion = $('#id_descripcion')

    this.$boton_buscar =  $('#boton_buscar')
    this.$boton_limpiar =  $('#boton_limpiar')

	this.init()
}
TargetaFiltros.prototype.init = function () {

    this.$padre.select2()
    this.$ubicacion.select2()

    this.$id.addClass('collapsed-box')

    this.$boton_buscar.on("click", this, this.click_BotonBuscar)
    this.$boton_limpiar.on("click", this, this.click_BotonLimpiar)
}
TargetaFiltros.prototype.get_Filtros = function (_page, _pageSize) {

    return {
        page: _page,
        pageSize: _pageSize,
        tag: this.$tag.val(),
        serie: this.$serie.val(),
        estado: this.$estado.val(),
        tipo: this.$tipo.val(),
        padre: this.$padre.val(),
        sistema: this.$sistema.val(),
        ubicacion: this.$ubicacion.val(),
        descripcion: this.$descripcion.val(),
    }
}

TargetaFiltros.prototype.get_FiltrosExcel = function () {

    return {
        tag: this.$tag.val(),
        serie: this.$serie.val(),
        estado: this.$estado.val(),
        tipo: this.$tipo.val(),
        padre: this.$padre.val(),
        sistema: this.$sistema.val(),
        ubicacion: this.$ubicacion.val(),
        descripcion: this.$descripcion.val(),
    }
}

TargetaFiltros.prototype.click_BotonBuscar = function(e) {

    e.preventDefault()
    targeta_resultados.grid.buscar()
}
TargetaFiltros.prototype.click_BotonLimpiar = function (e) {

    e.preventDefault()

    e.data.$tag.val("")
    e.data.$serie.val("")
    e.data.$estado.val("")
    e.data.$tipo.val("").trigger('change')
    e.data.$padre.val("").trigger('change')
    e.data.$sistema.val("")
    e.data.$ubicacion.val("").trigger('change')
    e.data.$descripcion.val("")
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
    this.kfuente_datos_excel = null

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
        tag: { type: "string" },
        descripcion: { type: "string" },
        serie: { type: "string" },
        especialidad: { type: "string" },
        estado: { type: "string" },
        tipo: { type: "string" },
        padre: { type: "string" },
        empresa: { type: "string" },
        sistema: { type: "string" },
        ubicacion: { type: "string" },
    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { field: "tag" , locked: true, title: "Tag", width: "120px" },
        { field: "descripcion" , title: "Descripcion", width: "250px" },
        { field: "serie" , title: "Serie", width: "120px" },
        { field: "especialidad" , title: "Especialidad", width: "120px" },
        { field: "tipo" , title: "Tipo", width: "120px" },
        { field: "estado" , title: "Estado", width: "120px" },
        { field: "padre" , title: "Padre", width: "370px" },
        { field: "empresa" , title: "Empresa", hidden: "true" },
        { field: "sistema" , title: "Sistema", width: "100px" },
        { field: "ubicacion" , title: "Ubicacion", width: "200px" },
        
        {
           command: [
                {
                   text: " Editar",
                   click: this.click_BotonEditar,
                   className: "boton_editar fa fa-pencil"
                },
                {
                    text: " Estructura",
                    click: this.click_BotonEstructura,
                    className: "boton_default fa fa-sitemap"
                },
                {
                    text: " Anexos",
                    click: this.click_BotonAnexos,
                    className: "boton_default fa fa-paperclip"
                }, 
                {
                    text: " Mediciones",
                    click: this.click_BotonMediciones,
                    className: "boton_default fa fa-area-chart"
                },                
            ],           
           title: " ",
           width: "430px"
        },        
    ]
}
GridPrincipal.prototype.apply_Estilos = function (e) {

    // Aplicar iconos
    e.sender.tbody.find(".k-button.fa.fa-pencil").each(function(idx, element){
        $(element).removeClass("fa fa-pencil").find("span").addClass("fa fa-pencil")
    })

    e.sender.tbody.find(".k-button.fa.fa-sitemap").each(function(idx, element){
        $(element).removeClass("fa fa-sitemap").find("span").addClass("fa fa-sitemap")
    })

    e.sender.tbody.find(".k-button.fa.fa-paperclip").each(function(idx, element){
        $(element).removeClass("fa fa-paperclip").find("span").addClass("fa fa-paperclip")
    })
    e.sender.tbody.find(".k-button.fa.fa-area-chart").each(function(idx, element){
        $(element).removeClass("fa fa-area-chart").find("span").addClass("fa fa-area-chart")
    })        

    // Aplicar formato a columna:
    $('td').each( function () {
        if($(this).text()=='TRABAJANDO'){ 
            $(this).addClass('cell--activo')
        }
        if($(this).text()=='DISPONIBLE'){ 
            $(this).addClass('cell--disponible')
        }        
        else if($(this).text()=='NO DISPONIBLE'){ 
            $(this).addClass('cell--deshabilitado')
        }
        else if($(this).text()=='EN REPARACION'){ 
            $(this).addClass('cell--reparacion')
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
    //this.kfuente_datos_excel.read()
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
GridPrincipal.prototype.click_BotonEstructura =  function (e) {
    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_estructura + fila.pk + "/"
}
GridPrincipal.prototype.click_BotonMediciones = function (e) {
    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_mediciones + fila.pk + "/odometros/"
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
            { value: 'Serie' },
            { value: 'Especialidad' },
            { value: 'Tipo' },
            { value: 'Estado' },
            { value: 'Padre' },
            { value: 'Sistema' },
            { value: 'Ubicacion' },
            
        ]
    }];
}
Toolbar.prototype.click_BotonExportar = function (e) {

    
    targeta_resultados.grid.leer_Datos()
    e.preventDefault()
    e.data.Inicializar_CeldasExcel()

    targeta_resultados.grid.kfuente_datos_excel.fetch(function () {

        var data = this.data();
        for (var i = 0; i < data.length; i++) {

            e.data.kRows.push({
                cells: [
                    { value: data[i].pk },
                    { value: data[i].tag },
                    { value: data[i].descripcion },
                    { value: data[i].serie },
                    { value: data[i].especialidad },
                    { value: data[i].tipo },
                    { value: data[i].estado },
                    { value: data[i].padre },
                    { value: data[i].sistema },
                    { value: data[i].ubicacion },
                    
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
                
                    ],
                    title: "Equipos",
                    rows: e.data.kRows
                }
            ]
        });
        kendo.saveAs({
            dataURI: workbook.toDataURL(),
            fileName: "Equipos.xlsx",
        });
    });
}