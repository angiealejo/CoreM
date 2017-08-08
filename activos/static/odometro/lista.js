/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_grid = window.location.origin + "/api/odometros/"
var url_excel = window.location.origin + "/api/odometroexcel/"
var url_nuevo = window.location.origin + "/odometros/nuevo/"
var url_editar = window.location.origin + "/odometros/editar/"
var url_medicion = window.location.origin + "/equipos/"

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

    this.$clave = $('#id_clave')
    this.$udm = $('#id_udm')
    this.$descripcion = $('#id_descripcion')
    this.$tipo = $('#id_tipo')
    this.$acumulado = $('#id_acumulado')

    this.$boton_buscar =  $('#boton_buscar')
    this.$boton_limpiar =  $('#boton_limpiar')

    this.init()
}
TargetaFiltros.prototype.init = function () {
    //this.$id.addClass('collapsed-box')
    this.$boton_buscar.on("click", this, this.click_BotonBuscar)
    this.$boton_limpiar.on("click", this, this.click_BotonLimpiar)
}
TargetaFiltros.prototype.get_Filtros = function (_page, _pageSize) {

    return {
        page: _page,
        pageSize: _pageSize,
        udm: this.$udm.val(),
        clave: this.$clave.val(),
        descripcion: this.$descripcion.val(),
        tipo: this.$tipo.val(),
        acumulado: this.$acumulado.val(),
    }
}
TargetaFiltros.prototype.click_BotonBuscar = function(e) {

    e.preventDefault()
    targeta_resultados.grid.buscar()
}
TargetaFiltros.prototype.click_BotonLimpiar = function (e) {

    e.preventDefault()
    e.data.$clave.val("")
    e.data.$descripcion.val("")
    e.data.$udm.val("").trigger('change')
    e.data.$acumulado.val("").trigger('change')
    e.data.$tipo.val("").trigger('change')
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
        clave: { type: "string" },
        descripcion: { type: "string" },
        udm: { type: "string" },
        
    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { field: "pk" , title: "Id", width: "80px" },
        { field: "clave" , title: "Clave", width: "120px" },
        { field: "descripcion" , title: "Descripción", width: "250px" },
        { field: "udm" , title: "UDM", width: "120px" },
        { field: "esta_activo" , title: "Activo", width: "120px" }, 
        { field: "acumulado" , title: "Acumulado", width: "120px" }, 
        { field: "tipo_odo" , title: "Tipo", width: "150px" }, 
        { field: "clasificacion" , title: "Clasificación", width: "150px" }, 

        {
           command: [
                {
                   text: " Editar",
                   click: this.click_BotonEditar,
                   className: "boton_editar fa fa-pencil"
                }, 
                // {
                //    text: " Mediciones",
                //    click: this.click_BotonMedicion,
                //    className: "boton_default fa fa-heartbeat"
                // },               
            ],           
           title: " ",
           width: "120px"
        },
    ]
}
GridPrincipal.prototype.apply_Estilos = function (e) {

    // Aplicar iconos
    e.sender.tbody.find(".k-button.fa.fa-pencil").each(function(idx, element){
        $(element).removeClass("fa fa-pencil").find("span").addClass("fa fa-pencil")
    })

    e.sender.tbody.find(".k-button.fa.fa-heartbeat").each(function(idx, element){
        $(element).removeClass("fa fa-heartbeat").find("span").addClass("fa fa-heartbeat")
    })    

    // Aplicar formato a columna:
    $('td').each( function () {
        if($(this).text()=='true'){ 

            $(this).addClass('cell--activo')
            $(this).text("Activo")
        }
        else if($(this).text()=='false'){ 
            $(this).addClass('cell--deshabilitado')
            $(this).text("Deshabilitado")
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
                    console.log("retorno algo el read")
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
GridPrincipal.prototype.click_BotonMedicion = function (e) {
    e.preventDefault()
    if (targeta_filtros.$equipo.val() == ''){
        
        alertify.warning("Especifique un equipo")
    }
    else{
        
        var fila = this.dataItem($(e.currentTarget).closest('tr'))
        window.location.href = url_medicion + fila.equipo + "/odometros/" + fila.pk + '/mediciones'

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
            { value: 'Clave' },
            { value: 'Descripcion' },
            { value: 'UDM' },
            { value: 'Activo' },
            { value: 'Acumulado' },
            { value: 'Tipo' },
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
                        { value: data[i].clave },
                        { value: data[i].udm },
                        { value: data[i].esta_activo },
                        { value: data[i].acumulado },
                        { value: data[i].tipo_odo },
                    
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
                    
                        ],
                        title: "Odometros",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "Odometros.xlsx",
            });
        });
}