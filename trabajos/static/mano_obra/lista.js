/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_manoobra = window.location.origin + "/api/manoobra/"
var url_ordenes = window.location.origin + "/api/ordenestrabajo/"
var url_empleados = window.location.origin + "/api/users/"

// OBJS
var targeta_resultados = null
var $ot_clave = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    $ot_clave = $('#ot_clave')

    targeta_resultados = new TargetaResultados()
    if (targeta_resultados.grid.$permiso.val() != "autenticado"){
        targeta_resultados.toolbar.ocultar_BotonNuevo()
        targeta_resultados.grid.ocultar_Botones()
    }
})



/*-----------------------------------------------*\
            OBJETO: RESULTADOS
\*-----------------------------------------------*/

function TargetaResultados() {

    this.toolbar = new Toolbar()
    this.grid = new GridPrincipal()
    this.modal = new VentanaModal()
}

/*-----------------------------------------------*\
            OBJETO: GRID
\*-----------------------------------------------*/

function GridPrincipal() {

	this.$id = $("#grid_principal")
    this.$permiso = $('#id_permiso')
    this.kfuente_datos = null
    this.kgrid = null

    this.init()
}
GridPrincipal.prototype.init = function () {

	kendo.culture("es-MX")

    this.kfuente_datos = new kendo.data.DataSource(this.get_FuenteDatosConfig())

    this.kgrid = this.$id.kendoGrid(this.get_Config())
}
GridPrincipal.prototype.ocultar_Botones = function () {

    var grid = this.kgrid.data("kendoGrid")
    grid.hideColumn(6)
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
        dataBound: this.apply_Estilos
    }
}
GridPrincipal.prototype.get_Campos = function (e) {

    return {

        empleado_desc : { type: "string" },
        descripcion : { type: "string" },
        fecha_inicio : { type: "date" },
        fecha_fin : { type: "date" },
        horas_estimadas : { type: "string" },
        horas_reales : { type: "string" },
    }
}
GridPrincipal.prototype.get_Columnas = function (e) {

    return [
        { field: "empleado_desc", title: "Empleado", width: "300px" },
        { field: "horas_estimadas", title: "Horas Estimadas"},
        { field: "horas_reales", title: "Horas Reales"},        
        { field: "fecha_inicio", title: "Fecha Inicio", format: "{0:dd-MMMM-yyyy}" },
        { field: "fecha_fin", title: "Fecha Fin", format: "{0:dd-MMMM-yyyy}" },
        { field: "descripcion", title: "Descripcion"},        
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
GridPrincipal.prototype.apply_Estilos = function (e) {

    // Aplicar iconos
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
                url: url_manoobra,
                type: "GET",
                dataType: "json",
            },
            parameterMap: function (data, action) {
                if (action === "read") {

                    return {
                        orden: $ot_clave.text()
                    }
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
    targeta_resultados.modal.set_Id(fila.pk)
    targeta_resultados.modal.mostrar()
}
GridPrincipal.prototype.click_BotonEliminar = function (e) {

    e.preventDefault()
    var fila = this.dataItem($(e.currentTarget).closest('tr'))

    alertify.confirm(
        'Eliminar Registro',
        '¿Desea Eliminar este registro?', 
        function () {

            var url = url_manoobra + fila.pk + "/"

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

    this.init()
}
Toolbar.prototype.init = function (e) {

    //this.$boton_exportar.on("click", this, this.click_BotonExportar)
}

Toolbar.prototype.ocultar_BotonNuevo = function () {
    this.$boton_nuevo.addClass("hidden")
}


/*-----------------------------------------------*\
            OBJETO: Ventana Modal
\*-----------------------------------------------*/

function VentanaModal() {

    this.$id = $('#win_modal')

    this.$pk = $("#modal_record_id")

    this.$empleado = $('#mod_empleado')
    this.$empleado_contenedor = $('#mod_empleado_contenedor')
    this.$empleado_mensaje =  $('#mod_empleado_mensaje')    

    this.$desc =  $('#mod_desc')

    this.$fecha_inicio = $('#mod_fecha_inicio')
    this.$fecha_fin = $('#mod_fecha_fin')

    this.$hrs_est = $('#mod_hrs_est')

    this.$hrs_real = $('#mod_hrs_real')

    this.$boton_guardar = $('#btn_modal_save')

    this.init()
}
VentanaModal.prototype.init = function () {

    this.$empleado.select2()

    // this.$fecha_inicio.datepicker(this.get_DateConfig())
    // this.$fecha_inicio.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})

    // this.$fecha_fin.datepicker(this.get_DateConfig())
    // this.$fecha_fin.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    
    // Se asoscia eventos al abrir el modal
    this.$id.on('show.bs.modal', this, this.load)
}
VentanaModal.prototype.get_DateConfig = function (){

    return {
        autoclose: true,
        language: 'es',
        todayHighlight: true,
        clearBtn: true,
        startDate: '2017-01-01',
    }
}
VentanaModal.prototype.set_Id = function (_value) {

    this.$pk.val(_value)
}
VentanaModal.prototype.mostrar = function (e) {
    this.$id.modal()
}
VentanaModal.prototype.clear_Fields = function () {

    this.$empleado.empty()
    this.$desc.val("")
    this.$fecha_inicio.val("")
    this.$fecha_fin.val("")
    this.$hrs_est.val("")
    this.$hrs_real.val("")
}
VentanaModal.prototype.clear_Estilos = function () {
    
    this.$empleado_contenedor.removeClass("has-error")
    if(this.$empleado_mensaje.hasClass('hidden') != null) { 
        this.$empleado_mensaje.addClass('hidden')
    }
}
VentanaModal.prototype.validar = function () {

    var bandera = true

    if ( this.$empleado.val() == "") {
        this.$empleado_contenedor.addClass("has-error")
        this.$empleado_mensaje.removeClass("hidden")
        bandera = false
    }

    return bandera
}
VentanaModal.prototype.fill_Empleados = function (_value, _selected) {

    combo_box = this.$empleado

    // Obtenemos articulos
    $.ajax({
        url: url_empleados,
        data: {
            "is_active" :  _value
        },
        method: "GET",
        success: function (response) {

            combo_box.append($('<option>', { 
                value: "",
                text : "-----------"
            }))            

            $.each(response, function (i, item) {
                 combo_box.append($('<option>', { 
                    value: item.pk,
                    text : "descripcion".replace("descripcion", item.full_name)
                }))
            })

            combo_box.trigger('change')

            combo_box.val(_selected).trigger('change')
        },
        error: function (response) {
            
            alertify.error("Ocurrio error al consultar")
        }
    })    
}
VentanaModal.prototype.load = function (e) {


    e.data.$fecha_inicio.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    e.data.$fecha_inicio.datepicker(e.data.get_DateConfig()).on('show.bs.modal', function(event) {
        event.stopPropagation()
    })
    // e.data.$fecha_inicio

    e.data.$fecha_fin.inputmask("yyyy-mm-dd", {"placeholder": "yyyy-mm-dd"})
    e.data.$fecha_fin.datepicker(e.data.get_DateConfig()).on('show.bs.modal', function(event) {
        event.stopPropagation()
    })
    // e.data.$fecha_fin.datepicker.on('show.bs.modal', function(event) {
    //     event.stopPropagation()
    // })
    
    // Se eliminan eventos viejos
    e.data.$boton_guardar.off("click")

    // Se limpian estilos
    e.data.clear_Estilos()

    // Se limpiar el formulario
    e.data.clear_Fields()  

    // Asosciar Eventos segun corresponda
    var event_owner
    
    // Edicion
    if ( e.relatedTarget == undefined ) {

        // Se modifica el titulo
        e.data.$id.find('.modal-title').text('Editar Servicio')

        // Se busca el registro y se llenan los controles
        modal = e.data

        $.ajax({
            url: url_manoobra,
            method: "GET",
            data: {
                "id": e.data.$pk.val()
            },
            success: function (response) {

                modal.$empleado.val(response[0].empleado_id)
                modal.$desc.val(response[0].descripcion)
                modal.$fecha_inicio.val(response[0].fecha_inicio)
                modal.$fecha_fin.val(response[0].fecha_fin)
                modal.$hrs_est.val(response[0].horas_estimadas)
                modal.$hrs_real.val(response[0].horas_reales)

                modal.fill_Empleados("", response[0].empleado_id)
            },
            error: function (response) {
                
                alertify.error("Ocurrio error al consultar")
            }
        })
        // Se asoscia el evento que se utilizara para guardar
        e.data.$boton_guardar.on(
            "click", 
            e.data, 
            e.data.editar
        )        
    }
    // Agregar
    else {

        e.data.fill_Empleados("true")

        event_owner = $(e.relatedTarget) 

        if (event_owner.context.id == "boton_nuevo") {

            // Se modifica el titulo
            e.data.$id.find('.modal-title').text('Nuevo registro')
            
            // Se asoscia el evento que se utilizara para guardar
            e.data.$boton_guardar.on(
                "click", 
                e.data, 
                e.data.nuevo
            )
        }        
    }
}
VentanaModal.prototype.nuevo = function (e) {

    if (e.data.validar()) {

        $.ajax({
            url: url_manoobra,
            method: "POST",
            data: {
                "orden" :  url_ordenes + $ot_clave.text() + "/",
                "empleado" : url_empleados + e.data.$empleado.val() + "/",

                "descripcion" : e.data.$desc.val(),
                "fecha_inicio" : e.data.$fecha_inicio.val(),
                "fecha_fin" : e.data.$fecha_fin.val(),
                "horas_estimadas" : e.data.$hrs_est.val(),
                "horas_reales" : e.data.$hrs_real.val(),
            },
            success: function (response) {

                alertify.success("Registro exitosamente guardado")

                targeta_resultados.grid.kfuente_datos.read()

                // Ocultar Modal
                e.data.$id.modal('hide')

            },
            error: function (response) {

                if (response.readyState == 4 && response.status == 500) {
                    alertify.error("El registro ya existe en la BD")
                }
                else {
                    alertify.error("Ocurrio error al modificar registro")
                }
            }
        })
    }
}
VentanaModal.prototype.editar = function (e) {

    if (e.data.validar()) {

        var url_update = url_manoobra + e.data.$pk.val() + "/"

        $.ajax({
            url: url_update,
            method: "PUT",
            data: {
                "orden" :  url_ordenes + $ot_clave.text() + "/",
                "empleado" : url_empleados + e.data.$empleado.val() + "/",
                
                "descripcion" : e.data.$desc.val(),
                "fecha_inicio" : e.data.$fecha_inicio.val(),
                "fecha_fin" : e.data.$fecha_fin.val(),
                "horas_estimadas" : e.data.$hrs_est.val(),
                "horas_reales" : e.data.$hrs_real.val(),
            },
            success: function (response) {

                alertify.success("Registro exitosamente guardado")

                targeta_resultados.grid.kfuente_datos.read()

                e.data.$id.modal('hide')
            },
            error: function (response) {

                if (response.readyState == 4 && response.status == 500) {
                    alertify.error("El registro ya existe en la BD")
                }
                else {
                    alertify.error("Ocurrio error al modificar registro")
                }
            }
        })
    }
}
