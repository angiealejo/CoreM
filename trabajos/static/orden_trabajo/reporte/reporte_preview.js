/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/
var url_empresas = window.location.origin + "/api/empresas/"
var url_reporte_pdf = window.location.origin + "/ordenes/reporte/pdf/orden_id/empresa/empresa_id/"

// OBJETOS
var reporte = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).on('ready', function() {
	
	reporte = new Reporte()

})

/*-----------------------------------------------*\
				OBJETO: REPORTE
\*-----------------------------------------------*/
function Reporte () {
	this.$boton_imprimir = $('#boton_imprimir')
	this.$logo = $('#id_logo')
	this.$empresa = $('#id_empresa')
    this.$ot = $('#caja_ot_id')
	this.init()
}

Reporte.prototype.init = function () {
	this.llenar_ComboEmpresa()
	this.$empresa.on('change', this, this.cambiar_Logo)
	this.$boton_imprimir.on('click', this, this.click_BotonImprimir)
}
Reporte.prototype.llenar_ComboEmpresa = function () {
	combo_empresa = this.$empresa

    $.ajax({
        url: url_empresas,
        data: {},
        method: "GET",
        success: function (response) {

            combo_empresa.append($('<option>', { 
                value: 0,
                text : "-----------"
            }))            

            $.each(response, function (i, item) {
                
                 combo_empresa.append($('<option>', { 
                    value: item.pk,
                    text : "descripcion".replace("descripcion", item.descripcion)
                }))
            })

        },
        error: function (response) {
            
            alertify.error("Ocurrio error al consultar")
        }
    })	
}
Reporte.prototype.cambiar_Logo  = function (e) {
	console.log(e.data.$empresa.val())
	$.ajax({
            url: url_empresas,
            method: "GET",
            data: {
                "id": e.data.$empresa.val()
            },
            success: function (response) {
            	//console.log(response)
                e.data.$logo.attr('src', response[0].logo)

            },
            error: function (response) {
                
                alertify.error("Ocurrio error al consultar")
            }
        })
}
Reporte.prototype.click_BotonImprimir = function (e) {

    var id_ot = e.data.$ot.val()
    var id_empresa = e.data.$empresa.val()
    var url = url_reporte_pdf.replace("orden_id", id_ot)
    var url = url.replace("empresa_id", id_empresa)

    if (id_empresa == 0) 
    {
        alertify.warning("Favor de especificar la empresa con la que se desea imprimir el reporte")
    }
    else {
        window.location.href = url;
    }
}