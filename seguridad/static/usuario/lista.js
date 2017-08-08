/*-----------------------------------------------*\
            GLOBAL VARIABLES
\*-----------------------------------------------*/

// URLS
var url_excel = window.location.origin + "/api/profilesexcel/"

// OBJS
var targeta_resultados = null

/*-----------------------------------------------*\
            LOAD
\*-----------------------------------------------*/

$(document).ready(function () {

    targeta_resultados = new TargetaResultados()
})

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

    this.kfuente_datos_excel = null

    this.init()
}
GridPrincipal.prototype.init = function () {

	kendo.culture("es-MX")

    this.kfuente_datos_excel = new kendo.data.DataSource(this.get_FuenteDatosExcel())
}


GridPrincipal.prototype.get_FuenteDatosExcel = function (e) {

    return {

        transport: {
            read: {

                url: url_excel,
                type: "GET",
                dataType: "json",
            },
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
GridPrincipal.prototype.get_Campos = function (e) {

    return {
        usuario: { type: "string" },
        full_name: { type: "string" },
        correo: { type: "string" },
        puesto: { type: "string" },
        clave: { type: "string" },
        fecha_nacimiento: { type: "string" },
        comentarios: { type: "string" },

    }
}
GridPrincipal.prototype.leer_Datos = function() {
    
    this.kfuente_datos_excel.read()
}

/*-----------------------------------------------*\
            OBJETO: TOOLBAR
\*-----------------------------------------------*/

function Toolbar() {

    this.$boton_exportar = $("#boton_exportar")

    this.init()
}
Toolbar.prototype.init = function (e) {

    this.$boton_exportar.on("click", this, this.click_BotonExportar)
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
            { value: 'Usuario' },
            { value: 'Nombre' },
            { value: 'Correo' },
            { value: 'Puesto' },
            { value: 'Clave' },
            { value: 'Fecha de Nacimiento'},
            { value: 'Comentarios' },
            
        ]
    }];
}
Toolbar.prototype.click_BotonExportar = function (e) {

    
    targeta_resultados.grid.leer_Datos()
    e.preventDefault();
    e.data.Inicializar_CeldasExcel();

        targeta_resultados.grid.kfuente_datos_excel.fetch(function () {

            var data = this.data();
            for (var i = 0; i < data.length; i++) {

                e.data.kRows.push({
                    cells: [
                        { value: data[i].pk },
                        { value: data[i].username },
                        { value: data[i].full_name },
                        { value: data[i].email },
                        { value: data[i].puesto },
                        { value: data[i].clave },
                        { value: data[i].fecha_nacimiento },
                        { value: data[i].comentarios },
                        
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
                    
                        ],
                        title: "Usuarios",
                        rows: e.data.kRows
                    }
                ]
            });
            kendo.saveAs({
                dataURI: workbook.toDataURL(),
                fileName: "Usuarios.xlsx",
            });
        });
}