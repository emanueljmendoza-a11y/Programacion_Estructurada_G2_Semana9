from flask import Flask, render_template, request, redirect, url_for, flash
import logica

app = Flask(__name__)
app.secret_key = "clave-solo-para-practica-local"  # necesaria para flash()


def contexto(**extra):
    datos = {
        "pendientes": logica.cola_pendientes,
        "historial": logica.pila_historial,
        "siguiente": logica.consultar_siguiente(),
        "stats": logica.estadisticas(),
        "busqueda": None,
        "id_buscado": None,
    }
    datos.update(extra)
    return datos


@app.get("/")
def inicio():
    return render_template("index.html", **contexto())


@app.get("/buscar")
def buscar():
    id_buscado = request.args.get("id", type=int)
    if id_buscado is None:
        flash("Escribe un ID numérico válido.", "warning")
        return redirect(url_for("inicio"))
    resultado = logica.buscar_por_id(id_buscado)
    return render_template("index.html",
                           **contexto(busqueda=resultado, id_buscado=id_buscado))


@app.post("/registrar")
def registrar():
    cliente = request.form.get("cliente", "")
    asunto = request.form.get("asunto", "")
    if logica.existe_pendiente(cliente, asunto):
        flash("Esa solicitud ya está pendiente.", "warning")
    elif logica.registrar_solicitud(cliente, asunto):
        flash("Solicitud registrada.", "success")
    else:
        flash("Cliente y asunto son obligatorios.", "danger")
    return redirect(url_for("inicio"))


@app.post("/atender")
def atender():
    if logica.atender_siguiente():
        flash("Solicitud atendida.", "success")
    else:
        flash("No hay solicitudes pendientes.", "warning")
    return redirect(url_for("inicio"))


@app.post("/deshacer")
def deshacer():
    if logica.deshacer_ultima_atencion():
        flash("Última atención deshecha.", "success")
    else:
        flash("No hay atenciones que deshacer.", "warning")
    return redirect(url_for("inicio"))


@app.post("/cancelar/<int:id>")
def cancelar(id):
    if logica.cancelar_solicitud(id):
        flash(f"Solicitud #{id} cancelada.", "success")
    else:
        flash(f"No existe la solicitud pendiente #{id}.", "warning")
    return redirect(url_for("inicio"))


@app.post("/deshacer-varias")
def deshacer_varias():
    cantidad = request.form.get("cantidad", type=int)
    if cantidad is None or cantidad < 1:
        flash("Escribe un número entero mayor que 0.", "danger")
    else:
        n = logica.deshacer_varias(cantidad)
        flash(f"Se restauraron {n} solicitudes.", "info")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)