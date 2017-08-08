/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_grid = window.location.origin + "/api/mediciones/"
var url_excel = window.location.origin + "/api/medicionexcel/"
var targeta_filtros = null
var targeta_resultados = null

// OBJS
var modal= null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    targeta_filtros = new TargetaFiltros()
    targeta_resultados = new TargetaResultados()
    modal = new Modal()


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

	this.$odometro = $('#id_odometro_requested') 
    this.$lectura_minima = $('#lectura_minima')
    this.$lectura_maxima = $('#lectura_maxima')
    this.$fecha_inicio = $('#fecha_inicio')
    this.$fecha_fin = $('#fecha_fin')
    this.$datepicker_formulario = $('#id_fecha')
    this.$boton_buscar =  $('#boton_buscar')
    this.$boton_limpiar =  $('#boton_limpiar')

	this.init()
}
TargetaFiltros.prototype.init = function () {

    //this.$odometro.select2()

    this.$id.addClass('collapsed-box')
    this.$fecha_inicio.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha_inicio.datepicker(this.get_DateConfig())
    this.$fecha_fin.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha_fin.datepicker(this.get_DateConfig())

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
        odometro: this.$odometro.val(),
        fecha_inicio: this.$fecha_inicio.val(),
        fecha_fin: this.$fecha_fin.val(),
        lectura_minima: this.$lectura_minima.val(),
        lectura_maxima: this.$lectura_maxima.val(),
        
    }
}
TargetaFiltros.prototype.click_BotonBuscar = function(e) {

    e.preventDefault()
    targeta_resultados.grid.buscar()
    
}
TargetaFiltros.prototype.click_BotonLimpiar = function (e) {

    e.preventDefault()
    //e.data.$odometro.val("").trigger('change')
    e.data.$lectura_minima.val("")
    e.data.$lectura_maxima.val("")
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
        odometro: { type: "string" },
        udm: { type: "string" },
        equipo: { type: "string"},
        fecha: { type: "date"},
        lectura: { type: "string" },
    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { 
            field: "fecha",
            title: "Fecha", 
            width: "120px", 
            format: "{0:dd-MMMM-yyyy hh:mm:ss tt}",
        },
        { field: "lectura" , title: "Lectura", width: "120px" },
        { field: "udm" , title: "Unidad de Medida", width: "120px" },

        {
           command: [
                {
                   text: " Eliminar",
                   click: this.click_BotonEliminar,
                   className: "boton_eliminar fa fa-trash-o"
                },              
            ],           
           title: " ",
           width: "40px"
        },
    ]
}
GridPrincipal.prototype.set_Icons = function (e) {

    e.sender.tbody.find(".k-button.fa.fa-trash-o").each(function(idx, element){
        $(element).removeClass("fa fa-trash-o").find("span").addClass("fa fa-trash-o")
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

GridPrincipal.prototype.click_BotonEliminar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    
    alertify.confirm(
        'Eliminar Registro',
        '¿Desea Eliminar este registro?', 

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

/*-----------------------------------------------*\
            OBJETO: TOOLBAR
\*-----------------------------------------------*/

function Toolbar() {

    this.$boton_exportar = $("#boton_exportar")
    this.$boton_nuevo = $("#boton_nuevo")

    this.init()
}
Toolbar.prototype.init = function (e) {

    this.$boton_exportar.on("click", this, this.click_BotonExportar)
    this.$boton_nuevo.on("click", this, this.click_BotonNuevo)
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
            { value: 'Id'},
            { value: 'Odometro' },
            { value: 'Equipo' },
            { value: 'UDM' },
            { value: 'Fecha' },
            { value: 'Lectura' },
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
                        { value: data[i].odometro_clave },
                        { value: data[i].equipo },
                        { value: data[i].udm },
                        { value: data[i].fecha },
                        { value: data[i].lectura },
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
                        title: "Mediciones",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "Mediciones.xlsx",
            });
        });
}

/*-----------------------------------------------*\
            OBJETO: MODAL
\*-----------------------------------------------*/

function Modal() {

    this.$odometro_medicion = $("#id_odometro_requested")
    this.$fecha_medicion = $("#id_fecha")
    this.$hora_medicion =$("#id_hora")
    this.$lectura_medicion = $("#id_lectura")
    this.$boton_guardar = $("#boton_guardar")
    this.$fecha_contenedor = $("#fecha_contenedor")
    this.$fecha_mensaje = $("#fecha_mensaje")
    this.$hora_contenedor = $("#hora_contenedor")
    this.$hora_mensaje = $("#hora_mensaje")
    this.$lectura_contenedor = $("#lectura_contenedor")
    this.$lectura_mensaje = $("#lectura_mensaje")
    
    this.init()
}

Modal.prototype.init = function (e) {
    
    this.$fecha_medicion.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    this.$fecha_medicion.datepicker(
        {
            autoclose: true,
            language: 'es',
            todayHighlight: true,
            clearBtn: true,
            startDate: '2017-01-01',
        }
    )
    this.$fecha_medicion.datepicker(
        "setDate", new Date()
    )

    this.$hora_medicion.timepicker(
        {
            showInputs: false
        }
    )
    
    this.$boton_guardar.on("click", this, this.click_BotonGuardar)
    this.clear_Estilos()
}
Modal.prototype.clear_Estilos = function () {
    
    this.$fecha_contenedor.removeClass("has-error")
    
    if(this.$fecha_mensaje.hasClass('hidden') != null) { 
        this.$fecha_mensaje.addClass('hidden')
    } 

    this.$lectura_medicion.removeClass("has-error")  

    if(this.$lectura_mensaje.hasClass('hidden') != null) { 
        this.$lectura_mensaje.addClass('hidden')
    } 
}

Modal.prototype.validar = function () {

    var bandera = true

    if ( this.$fecha_medicion.val() == "") {
        this.$fecha_contenedor.addClass("has-error")
        this.$fecha_mensaje.removeClass("hidden")
        bandera = false
    }

    if ( this.$hora_medicion.val() == "") {
        this.$hora_contenedor.addClass("has-error")
        this.$hora_mensaje.removeClass("hidden")
        bandera = false
    }

    if ( this.$lectura_medicion.val() == "") {
        this.$lectura_contenedor.addClass("has-error")
        this.$lectura_mensaje.removeClass("hidden")
        bandera = false
    }

    return bandera
}
Modal.prototype.get_Hora = function (_hora){
    this.hora = _hora
    var horas = parseInt(this.hora.substr(0, 2))

    if(this.hora.indexOf('am') != -1) {
        this.hora = this.hora.replace('12', '0')
        
    }
    if(this.hora.indexOf('pm')  != -1) {
        if(horas<10){
            
            this.hora = this.hora.replace(horas, (horas + 12))
            this.hora = this.hora.substr(1, 5)

        }
        else if(horas==12){

            this.hora = this.hora
        }
        else{

            this.hora = this.hora.replace(horas, (horas + 12))
            
        }
           
    }
        this.hora = this.hora.replace(/(am|pm)/, '')
        return this.hora
        
}

Modal.prototype.click_BotonGuardar = function(e) {
    if (e.data.validar()){

        e.preventDefault()
        odometro_medicion = e.data.$odometro_medicion.val()
        fecha_medicion = e.data.$fecha_medicion.val()
        hora_medicion = e.data.$hora_medicion.val().toLowerCase()
        hora_medicion =e.data.get_Hora(hora_medicion).trim()
        hora_medicion = "T"+hora_medicion+":00"
        lectura_medicion = e.data.$lectura_medicion.val()
        console.log(odometro_medicion)
        console.log(fecha_medicion)
        console.log(lectura_medicion)
        console.log(hora_medicion)
        $.ajax({
                url: url_grid,
                method: "POST",
                data: {
                    odometro: odometro_medicion,
                    lectura: lectura_medicion,
                    fecha: fecha_medicion+hora_medicion,
                },
                success: function (){
                    $('#modal_nuevo').modal('hide');
                    alertify.success("Se registró medición correctamente")
                    targeta_resultados.grid.kfuente_datos.read();
                    e.data.$lectura_medicion.val("")
                   
                },
                error: function(e){

                    alertify.error("Error "+ e.status + " . No se guardó el registro")
                    $('#modal_nuevo').modal('hide')
                }
               
                        
            });
    } 
}