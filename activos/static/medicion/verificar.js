/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/
//location.reload();
// URLS
var url_historico = window.location.origin + "/equipos/"
var url_medicion = window.location.origin + "/api/mediciones/"
var url_excel = window.location.origin + "/api/medicionexcel/"
var url_equipo = window.location.origin + "/api/equipoexcel/"
var url_detalle = window.location.origin + "/equipos/"
var url_grid = window.location.origin + "/api/mediciones/"
var url_historial = window.location.origin + "/mediciones/log/"
// OBJS
var tabla = null
var modal = null
/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {
    filtros = new Filtros()
    filtros.llenar_SelectEquipos()
    tabla = new Tabla()
    toolbar = new Toolbar()
    grid_historico = new GridHistorico()

})

/*-----------------------------------------------*\
            OBJETO: FILTROS
\*-----------------------------------------------*/
function Filtros () {
    this.$tipo_equipo = $('#id_tipo_equipo')
    this.$equipo = $('#id_equipo')
    this.$equipo_texto = $('#equipo_texto')
    this.$equipo_id = $('#equipo_id')
    this.$fecha_inicio = $('#id_fecha_inicio')
    this.$fecha_fin = $('#id_fecha_fin')
    this.$tipo = $('#id_tipo')
    this.$boton_limpiar = $('#boton_limpiar')
    this.$boton_buscar = $('#boton_buscar')
    this.$tipo_odometro = $('#tipo_odometro')
    this.init()
}
Filtros.prototype.init = function () {
    this.$equipo.select2(

    )
    this.$fecha_inicio.datetimepicker(this.get_DateConfig());
    this.$fecha_fin.datetimepicker(this.get_DateConfig());
    this.$boton_limpiar.on('click', this, this.click_BotonLimpiar)
    this.$tipo_equipo.on('change', this, this.change_TipoEquipo)
    this.$equipo.on('select2:select', this, this.select_Equipo)

}
Filtros.prototype.get_DateConfig = function () {
    return {
            locale: 'es',
            format: "YYYY-MM-DD HH:mm",
            minDate: "2017-01-01 00:00",
            stepping: 60,
            defaultDate: new Date(),
            sideBySide: true,
        }
    
}
Filtros.prototype.click_BotonLimpiar = function (e) {
    e.preventDefault()
    e.data.$tipo.val(0).trigger('change')
    e.data.$fecha_inicio.val("")
    e.data.$fecha_fin.val("")
}
Filtros.prototype.select_Equipo = function (e) {
    if (e.data.$equipo.val() != 0){
        e.data.$boton_buscar.prop('disabled', false)
    }
    else if (e.data.$equipo.val() == 0){
        e.data.$boton_buscar.prop('disabled', true)
    }
    
}
Filtros.prototype.llenar_SelectEquipos = function () {
    filtros.$equipo.find('option').remove().end().append($('<option>').attr('value', 0).text("Seleccione..."))

    $.ajax({
            url: url_equipo,
            method: "GET",
            data: {
                "tipo": filtros.$tipo_equipo.val()
            },
            success: function (response) {
            $.each(response, function(index, item) 
                {   
                    filtros.$equipo.append($('<option>').attr('value',item.pk).text("("+item.tag+") "+item.descripcion))
                    filtros.$equipo.trigger('change')
                }
            )
            filtros.$equipo.val(filtros.$equipo_id.val())
            filtros.$equipo.trigger('change')
                
            },
            error: function () {

                alertify.error("Ocurrió un error al consultar los equipos")
            }
    })
}
Filtros.prototype.change_TipoEquipo = function (e) {
    e.preventDefault()
    var event_owner = $(this)
    filtros.$equipo.find('option').remove().end().append($('<option>').attr('value', 0).text("Seleccione..."))

    $.ajax({
            url: url_equipo,
            method: "GET",
            data: {
                "tipo": event_owner.val()
            },
            success: function (response) {
            $.each(response, function(index, item) 
                {   
                    filtros.$equipo.append($('<option>').attr('value',item.pk).text("("+item.tag+") "+item.descripcion))
                    filtros.$equipo.trigger('change')
                }
            )
                
            },
            error: function () {

                alertify.error("Ocurrió un error al consultar los equipos")
            }
    })
}
/*-----------------------------------------------*\
            OBJETO: TABLA
\*-----------------------------------------------*/
function Tabla () {
    this.modal_historico = new ModalHistorico()
    this.$titulo_odometro = $("strong[data-tipo='titulo-odometro']")
    this.$celda_suma = $("strong[data-suma='suma']")
    this.$celda_horas = $("strong[data-horas='horas']")
    this.$boton_historial = $('#boton_historial')
    this.$celdas_tiempo = $("[data-celda='tiempo']")
    this.event_owner = null
    this.odometro = null
    this.equipo = null
    this.init()

}
Tabla.prototype.init = function () {
    this.$titulo_odometro.on('mouseover', this, this.OnCell)
    this.$titulo_odometro.on('mouseout', this, this.OffCell)
    this.$titulo_odometro.on('click', this, this.click_TituloOdometro)
    this.$boton_historial.on('click', this, this.click_BotonHistorial)
    this.$celda_suma.each(function() {
        var suma = 0
        $(this).parents("tr").find('.odometro').each(function() {
            suma += parseFloat($(this).text())
        })

      $(this).text(suma)
      $(this).addClass('corem-text-normal')
    })

    this.$celda_horas.each(function() {
        var suma = 0
        $(this).parents("tr").find('.odometro').each(function() {
            suma += parseFloat($(this).text())
        })
        horas = parseInt(suma / 60)
        minutos = suma % 60
      $(this).text(horas + " horas, " + minutos + " minutos")
      $(this).addClass('corem-text-normal')
    })
    if (filtros.$tipo_odometro.val() != "COM_H"){
        this.$celdas_tiempo.addClass('hidden')
    }
}

Tabla.prototype.OnCell = function (e) {
    e.preventDefault()
    var event_owner = $(this)
    event_owner.addClass("corem-shadow")
}
Tabla.prototype.OffCell = function (e) {
    e.preventDefault()
    var event_owner = $(this)
    event_owner.removeClass("corem-shadow")
}
Tabla.prototype.click_TituloOdometro = function (e){
    e.preventDefault()
    e.data.event_owner = $(this)
    console.log($(this))
    id_odometro = e.data.event_owner.attr('data-id')
    odometro_texto = e.data.event_owner.text()
    e.data.odometro = id_odometro
    e.data.modal_historico.$odometro_texto.text("Odómetro: " + odometro_texto)
    e.data.modal_historico.load()
    e.data.modal_historico.$id.modal('show')
}
Tabla.prototype.click_BotonHistorial = function (e) {
    e.preventDefault()
    window.open(url_historial  + filtros.$equipo.val() + "/" + filtros.$tipo.val() + "/", '_blank')

}
Tabla.prototype.get_Filtros = function (_page, _pageSize){

    return {
        page: _page,
        pageSize: _pageSize,
        equipo: filtros.$equipo_id.val(),
        odometro: this.odometro,
        fecha_inicio_ver: tabla.modal_historico.filtros.$fecha_inicio.val(), 
        fecha_fin_ver: tabla.modal_historico.filtros.$fecha_fin.val()
        
    }
}
/*-----------------------------------------------*\
            OBJETO: FILTROS MODAL HISTORICO
\*-----------------------------------------------*/
function FiltrosModal () {
    this.$fecha_inicio = $('#fecha_inicio_modal')
    this.$fecha_fin = $('#fecha_fin_modal')
    this.$boton_limpiar = $('#modal_btn_limpiar')
    this.$boton_buscar = $('#modal_btn_buscar')
    this.init()
}
FiltrosModal.prototype.init = function () {
    this.$fecha_inicio.datetimepicker(this.get_DateConfig(filtros.$fecha_inicio.val()))
    this.$fecha_fin.datetimepicker(this.get_DateConfig(filtros.$fecha_fin.val()))
    this.$boton_limpiar.on('click', this, this.click_BotonLimpiar)
    this.$boton_buscar.on('click', this, this.click_BotonBuscar)
}
FiltrosModal.prototype.get_DateConfig = function (_fecha) {
    return {
            locale: 'es',
            format: "YYYY-MM-DD HH:mm",
            minDate: "2017-01-01 00:00",
            stepping: 60,
            sideBySide: true,
            defaultDate: _fecha
        }
    
}
FiltrosModal.prototype.click_BotonLimpiar = function (e) {
    e.preventDefault()
    e.data.$fecha_inicio.val("")
    e.data.$fecha_fin.val("")
}
FiltrosModal.prototype.click_BotonBuscar = function (e) {
    e.preventDefault()
    grid_historico.buscar()
}
/*-----------------------------------------------*\
            OBJETO: MODAL HISTORICO
\*-----------------------------------------------*/
function ModalHistorico () {
    this.filtros = new FiltrosModal()
    this.$id = $('#modal_historico')
    this.$contenido = $('#modal_contenido')
    this.$equipo = $('#id_eq')
    this.$odometro = $('#id_odo')
    this.$equipo_texto = $('#equipo_texto')
    this.$odometro_texto = $('#odo_texto')
    this.$fecha_texto = $('#fecha_texto')
    this.$udm = $('#id_udm')
    this.$usuario = $('#usuario')
    this.init()
}
ModalHistorico.prototype.init = function () {

    this.$contenido.addClass('corem-modal')

}
ModalHistorico.prototype.load = function () {
    grid_historico.kfuente_datos.page(1)
    grid_historico.kfuente_datos.read()
    grid_historico.kfuente_datos_excel.read()
}
/*-----------------------------------------------*\
            OBJETO: GRID HISTORICO
\*-----------------------------------------------*/
function GridHistorico () {
    this.$id = $('#grid_principal')
    this.kfuente_datos = null
    this.kfuente_datos_excel = null
    this.kgrid = null

    this.init()
}
GridHistorico.prototype.init = function () {

    kendo.culture("es-MX")

    this.kfuente_datos = new kendo.data.DataSource(this.get_FuenteDatosConfig())
    this.kfuente_datos_excel = new kendo.data.DataSource(this.get_FuenteDatosExcel())

    this.kGrid = this.$id.kendoGrid(this.get_Config())
}
GridHistorico.prototype.get_Config = function () {

    return {
        dataSource: this.kfuente_datos,
        columnMenu: false,
        groupable: false,
        sortable: false,
        editable: "inline",
        resizable: true,
        selectable: true,
        scrollable: false,
        columns: this.get_Columnas(),
        scrollable: true,
        pageable: true,
        dataBound: this.set_Icons,
        edit: function(e){
            e.container.find("td:eq(1) input").focus();
        },
        save: function(e) {
            
            e.preventDefault()
            if (e.model.equipo){
                var pk = e.model.pk
                var equipo = e.model.equipo
                var odometro = e.model.odometro
                var lectura = e.model.lectura
                var fecha = e.model.fecha
                var observaciones = e.model.observaciones
                var usuario = tabla.modal_historico.$usuario.val()

                nueva_fecha = new Date(
                    Date.UTC(
                        fecha.getFullYear(),
                        fecha.getMonth(),
                        fecha.getDate(), 
                        fecha.getHours(),
                        fecha.getMinutes(),
                        fecha.getSeconds()
                        )
                    )

                grid_historico.actualizar_Medicion(pk, equipo, odometro, lectura, nueva_fecha, observaciones, usuario)
                grid_historico.kfuente_datos.read()
                grid_historico.kfuente_datos_excel.read()
            }
            else {
                var equipo = filtros.$equipo_id.val()
                var odometro = tabla.$odometro
                var lectura = e.model.lectura
                var usuario = tabla.modal_historico.$usuario.val()
                var fecha = e.model.fecha
                nueva_fecha = new Date(
                    Date.UTC(
                        fecha.getFullYear(),
                        fecha.getMonth(),
                        fecha.getDate(), 
                        fecha.getHours(),
                        fecha.getMinutes(),
                        fecha.getSeconds()
                        )
                    )

    
                var observaciones = e.model.observaciones

                grid_historico.registrar_Medicion(equipo, odometro, lectura, nueva_fecha, observaciones, usuario)
                grid_historico.kfuente_datos.read()
                grid_historico.kfuente_datos_excel.read()
               
            }
        },
        cancel: function (e) {
            e.preventDefault()
            grid_historico.kfuente_datos.read()
        }
           
    }     
}

GridHistorico.prototype.get_Campos = function (e) {

    return {
        fecha: { type: "date" },
        lectura: { type: "string" },
        lectura: { type: "observaciones" },
        
    }
}
GridHistorico.prototype.get_Columnas = function (e) {

    return [
        { field: "fecha" ,
            title: "Fecha",
            width: "120px",
            format:"{0:dd-MMMM-yyyy HH:mm}",
            editor: this.timeEditor,
            validation: { required: true } },
        { field: "lectura" ,
          title: "Lectura",
          width: "120px",
          type: "number",
          validation: { min: 0, required: true },
          editor: this.editNumberWithoutSpinners,
          editable: true
        },
        { field: "observaciones", title: "Observaciones", width:"120px" },
        { field: "creado_por", title: "Creado por", width:"120px", IsNotEditable: true },
        { field: "modificado_por", title: "Modificado por", width:"120px", IsNotEditable: true },
        { command: 
            [
                {
                    name:"edit",
                    text:{
                            edit: "Editar",
                            update: "Actualizar", 
                            cancel: "Cancelar",
                        }
                },
                {
                   text: " Eliminar",
                   click: this.click_BotonEliminar,
                   className: "boton_eliminar fa fa-trash-o"
                },

            ],
            width: "180px"
        },


    ]
}
GridHistorico.prototype.get_ColumnasComentario = function (e) {

    return [
        { field: "fecha" ,
            title: "Fecha",
            width: "120px",
            format:"{0:dd-MMMM-yyyy HH:mm}",
            editor: this.timeEditor,
            validation: { required: true } },
        { field: "observaciones" ,
          title: "Lectura",
          width: "120px",
          type: "string",
        },
        { field: "creado_por", title: "Creado por", width:"120px", IsNotEditable: true },
        { field: "modificado_por", title: "Modificado por", width:"120px", IsNotEditable: true },
        { command: 
            [
                {
                    name:"edit",
                    text:{
                            edit: "Editar",
                            update: "Actualizar", 
                            cancel: "Cancelar",
                        }
                },
                {
                   text: " Eliminar",
                   click: this.click_BotonEliminar,
                   className: "boton_eliminar fa fa-trash-o"
                },

            ],
            width: "180px"
        },


    ]
}
GridHistorico.prototype.click_BotonEliminar = function (e) {
    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    
    alertify.confirm(
        'Eliminar Registro',
        '¿Desea Eliminar esta medicion?', 

        function () {

            var url = url_grid + fila.pk + "/"

            $.ajax({
                url: url,
                method: "DELETE",
                success: function () {
                    alertify.success("Se eliminó medición correctamente")

                    grid_historico.kfuente_datos.remove(fila)
                    
                },
                error: function () {
                    
                    alertify.error("Ocurrió un error al eliminar")
                }
            })
        }, 
        null
    )
}
GridHistorico.prototype.set_Icons = function (e) {

    e.sender.tbody.find(".k-button.fa.fa-trash-o").each(function(idx, element){
        $(element).removeClass("fa fa-trash-o").find("span").addClass("fa fa-trash-o")
    })
}
GridHistorico.prototype.timeEditor = function (container, options) {
    $('<input data-text-field="' + options.field + '" data-value-field="' + options.field + '" data-bind="value:' + options.field + '" data-format="' + options.format + '"/>')
            .appendTo(container)
            .kendoTimePicker({});
}
GridHistorico.prototype.editNumberWithoutSpinners = function (container, options) {
    $('<input data-text-field="' + options.field + '" ' +
            'data-value-field="' + options.field + '" ' +
            'data-bind="value:' + options.field + '" ' +
            'data-format="' + options.format + '"/>')
            .appendTo(container)
            .kendoNumericTextBox({
                spinners: false,
                format: "n6",
                decimals: 6,
                step: 0.000001,
            });
}
GridHistorico.prototype.get_FuenteDatosExcel = function (e) {

    return {

        transport: {
            read: {

                url: url_excel,
                type: "GET",
                dataType: "json",
            },
            parameterMap: function (data, action) {
                if (action === "read") {

                    return tabla.get_Filtros()
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
GridHistorico.prototype.get_FuenteDatosConfig = function (e) {

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

                    return tabla.get_Filtros(data.page, data.pageSize)
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
GridHistorico.prototype.registrar_Medicion = function (_equipo, _odometro, _lectura, _fecha, _observaciones, _usuario) {

    var url_create = url_grid 
    
    data = {
        'equipo': _equipo,
        'odometro': _odometro, 
        'lectura': _lectura,
        'fecha': _fecha,
        'observaciones': _observaciones,
        'created_by': _usuario,
    }

    $.ajax({

        url: url_create,
        data : JSON.stringify(data),
        dataType: "json",
        type: "POST",
        contentType: "application/json; charset=utf-8",

        success: function (e) {
            alertify.warning("Se guardó el registro")
        },
        error: function (e) {
            alertify.error("No se pudo guardar el registro")
        }
    })    

}
GridHistorico.prototype.actualizar_Medicion = function (_id, _equipo, _odometro, _lectura, _fecha, _observaciones, _usuario) {

    var url_update = url_grid + _id  + "/"
    
    data = {
        'equipo': _equipo,
        'odometro': _odometro, 
        'lectura': _lectura,
        'fecha': _fecha,
        'observaciones': _observaciones,
        'updated_by': _usuario,
    }

    $.ajax({

        url: url_update,
        data : JSON.stringify(data),
        dataType: "json",
        type: "PUT",
        contentType: "application/json; charset=utf-8",

        success: function (e) {
            alertify.warning("Se guardó el registro")
        },
        error: function (e) {
            alertify.error("No se pudo guardar el registro")
        }
    })    

}
GridHistorico.prototype.buscar =  function() {
    this.kfuente_datos.page(1)
    this.kfuente_datos_excel.read()
}
GridHistorico.prototype.click_BotonEditar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    window.location.href = url_editar + fila.pk + "/"
}
GridHistorico.prototype.click_BotonMedicion = function (e) {
    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))
    var id_odometro = fila.pk
    window.location.href = url_medicion + id_odometro + '/mediciones/'

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
    grid_historico.$id.data("kendoGrid").addRow();
}
Toolbar.prototype.Inicializar_CeldasExcel = function (e) {

    if (grid_historico.get_Columnas != null)
    {
        if (grid_historico.get_Columnas.length != 1) {
            grid_historico.get_Columnas.length = 0;
        }
    }

    this.kRows = [{
        cells: [
            { value: 'Fecha'},
            { value: 'Lectura' },
            { value: 'Observaciones' },
            { value: 'Creado por' },
            { value: 'Modificado por' },
        ]
    }];
}
Toolbar.prototype.click_BotonExportar = function (e) {

    e.preventDefault();
    e.data.Inicializar_CeldasExcel();

    
        grid_historico.kfuente_datos_excel.fetch(function () {

            var data = this.data();
            for (var i = 0; i < data.length; i++) {

                e.data.kRows.push({
                    cells: [
                        { value: data[i].fecha, format: "dd/MM/yyyy hh:mm" },
                        { value: data[i].lectura },
                        { value: data[i].observaciones },
                        { value: data[i].creado_por },
                        { value: data[i].modificado_por },
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
                        ],
                        title: "Hoja 1",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "reporte.xlsx"
            });
        });
}