/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_grid = window.location.origin + "/api/articulos/"
var url_excel = window.location.origin + "/api/articulos2/"
var url_nuevo = window.location.origin + "/articulos/nuevo/"
var url_editar = window.location.origin + "/articulos/editar/"
var url_anexos = window.location.origin + "/articulos/anexos/"
var url_stock = window.location.origin + "/stock/"

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

    this.$clave = $('#id_clave')
    this.$descripcion = $('#id_descripcion')
    this.$tipo = $('#id_tipo')
    this.$udm = $('#id_udm')
    this.$clave_jde = $('#id_clave_jde')

    this.$boton_buscar =  $('#boton_buscar')
    this.$boton_limpiar =  $('#boton_limpiar')

	this.init()
}
TargetaFiltros.prototype.init = function () {
    
    this.$udm.select2()

    this.$id.addClass('collapsed-box')

    this.$boton_buscar.on("click", this, this.click_BotonBuscar)
    this.$boton_limpiar.on("click", this, this.click_BotonLimpiar)
}
TargetaFiltros.prototype.get_Filtros = function (_page, _pageSize) {

    return {
        page: _page,
        pageSize: _pageSize,

        clave: this.$clave.val(),
        descripcion: this.$descripcion.val(),
        tipo: this.$tipo.val(),
        udm: this.$udm.val(),
        clave_jde: this.$clave_jde.val(),
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
    e.data.$tipo.val("")
    e.data.$udm.val("").trigger('change')
    e.data.$clave_jde.val("")

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
        columnMenu: true,
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
        tipo: { type: "string" },
        udm: { type: "string" },
        clave_jde: { type: "string" },
        marca: { type: "string" },
        modelo: { type: "string" },
        numero_parte: { type: "string" },
        stock_minimo: { type: "number" },
        stock_maximo: { type: "number" },
        stock_seguridad: { type: "number" },

    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { field: "descripcion", locked: false, lockable: true, title: "Descripcion", width: "450px" },
        { field: "clave",  title: "Clave", width: "120px" },
        { field: "udm", title: "UDM", width: "120px" },
        { field: "estado" , title: "Estado", width: "120px" },
        { field: "tipo", title: "Tipo", width: "120px" },

        { field: "marca", title: "Marca", width: "120px" },
        { field: "modelo", title: "Modelo", width: "120px" },
        { field: "numero_parte", title: "No. Parte", width: "120px" },

        { field: "clave_jde", title: "Clave JDE", width: "120px" },
        { field: "stock_minimo", title: "Stock Min.", width: "100px" },
        { field: "stock_maximo", title: "Stock Max.", width: "100px" },
        { field: "stock_seguridad", title: "Stock de Seg.", width: "100px" },
        { field: "observaciones", title: "Observaciones", width: "220px", format: '{0:n2}', encoded: false  },
        { field: "url", title: "URL", width: "220px", template: "#= targeta_resultados.grid.set_Url(url) #" },
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
                    text: " Anexos",
                    click: this.click_BotonAnexos,
                    className: "boton_default fa fa-paperclip"
                },                
            ],           
           title: " ",
           width: "260px"
        },
    ]
}
GridPrincipal.prototype.set_Url = function (_value) {

    if (_value) {
        return "<p><a target='_blank' rel='nofollow' href='"+_value +"'" + " >" + _value + "</a></p> "   
    }
    else {
        return ""
    }
}
GridPrincipal.prototype.apply_Estilos = function (e) {

    // Aplicar iconos
    e.sender.tbody.find(".k-button.fa.fa-pencil").each(function(idx, element){
        $(element).removeClass("fa fa-pencil").find("span").addClass("fa fa-pencil")
    })

    e.sender.tbody.find(".k-button.fa.fa-paperclip").each(function(idx, element){
        $(element).removeClass("fa fa-paperclip").find("span").addClass("fa fa-paperclip")
    })

    e.sender.tbody.find(".k-button.fa.fa-th-large").each(function(idx, element){
        $(element).removeClass("fa fa-th-large").find("span").addClass("fa fa-th-large")
    })        

    // Aplicar formato a columna:
    $('td').each( function () {
        if($(this).text()=='ACTIVO'){ 

            $(this).addClass('cell--activo')
        }
        else if($(this).text()=='DESHABILITADO'){ 
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
GridPrincipal.prototype.click_BotonAnexos = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_anexos + fila.pk + "/texto/"
}
GridPrincipal.prototype.click_BotonStock = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_stock + "0/" + fila.pk + "/"
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
            { value: 'Id' },
            { value: 'Clave' },
            { value: 'Descripcion' },
            { value: 'Tipo' },
            { value: 'Estado' },
            { value: 'UDM' },
            { value: 'Observaciones' },
            { value: 'Stock Minimo' },
            { value: 'Stock Maximo' },
            { value: 'Stock de seguridad' },
            { value: 'URL'},
            { value: 'Clave JDE' },

            
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
                        { value: data[i].descripcion },
                        { value: data[i].tipo },
                        { value: data[i].estado },
                        { value: data[i].udm },
                        { value: data[i].observaciones },
                        { value: data[i].stock_minimo },
                        { value: data[i].stock_maximo },
                        { value: data[i].stock_seguridad },
                        { value: data[i].url },
                        { value: data[i].clave_jde },
                        
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
                        ],
                        title: "Articulos",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "Articulo.xlsx",
            });
        });
}