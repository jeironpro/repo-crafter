import re
import secrets
import shutil
from collections import Counter
from datetime import date
from pathlib import Path

from flask import Flask, render_template, redirect, flash, request, jsonify, abort, Response
from flask_wtf import CSRFProtect

from config import GITHUB_USER, CARPETA_REPOS, YEAR
import github_api
import git_ops
import resumen

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

csrf = CSRFProtect(app)

# Validación de parámetros de ruta contra path traversal
VISIBILIDADES = {"publico", "privado"}
NOMBRE_REPO_RE = re.compile(r"^[A-Za-z0-9._-]{1,100}$")
TOPIC_RE = re.compile(r"^[a-z0-9-]{1,50}$")


def validar_nombre(nombre):
    if not NOMBRE_REPO_RE.match(nombre or ""):
        abort(404)
    return nombre


def ruta_repo(visibilidad, nombre):
    if visibilidad not in VISIBILIDADES:
        abort(404)
    validar_nombre(nombre)
    carpeta = CARPETA_REPOS / visibilidad / nombre
    if CARPETA_REPOS.resolve() not in carpeta.resolve().parents:
        abort(404)
    return carpeta


@app.route('/', methods=["GET", "POST"])
def index():
    contador_repo_privados = 0
    contador_repo_publicos = 0
    contador_paginas_creadas = 0
    topic_count = Counter()

    try:
        repos = github_api.obtener_repos()
    except RuntimeError as error:
        return str(error)

    templates_gitignore = github_api.obtener_templates_gitignore()

    for repo in repos:
        if repo["has_pages"]:
            contador_paginas_creadas += 1
        if repo["private"]:
            contador_repo_privados += 1
        else:
            contador_repo_publicos += 1

        topic_count.update(repo.get("topics", []))

    total_repos = contador_repo_publicos + contador_repo_privados

    return render_template(
        "index.html",
        repos=repos,
        repos_publicos=contador_repo_publicos,
        paginas_creadas=contador_paginas_creadas,
        repos_privados=contador_repo_privados,
        templates_gitignore=templates_gitignore,
        total_repos=total_repos,
        topic_count=topic_count,
        year=YEAR
    )


@app.route("/resumen", methods=["GET"])
def descargar_resumen():
    try:
        repos = github_api.obtener_repos()
    except RuntimeError as error:
        return str(error)

    grupos = resumen.clasificar_repos(repos)
    topics = {repo["name"]: resumen.topics_despliegue(repo) for repo in grupos["desplegados"]}

    tokens = (Path(app.root_path) / "static" / "css" / "tokens.css").read_text(encoding="utf-8")
    html = render_template(
        "resumen.html",
        grupos=grupos,
        topics_despliegue=topics,
        tokens=tokens,
        usuario=GITHUB_USER,
        fecha=date.today().strftime("%d/%m/%Y"),
        total=len(repos)
    )

    pdf = resumen.generar_pdf(html)
    return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={resumen.nombre_archivo()}"}
    )


@app.route("/topics/<nombre>", methods=["POST"])
def guarda_topics(nombre):
    validar_nombre(nombre)

    crudos = request.form.get("topics", "")
    topics = [topic.strip().lower() for topic in crudos.split(",") if topic.strip()]

    if len(topics) > 20:
        flash("Un repositorio puede tener como máximo 20 topics", "error")
        return redirect("/")

    invalidos = [topic for topic in topics if not TOPIC_RE.match(topic)]
    if invalidos:
        flash(f"Topics inválidos: {', '.join(invalidos)}. Solo minúsculas, números y guiones (máx. 50 caracteres)", "error")
        return redirect("/")

    respuesta = github_api.actualizar_topics(nombre, topics)

    if respuesta.status_code in [200, 204]:
        github_api.limpiar_cache()
        flash(f"Topics de '{nombre}' actualizados correctamente", "success")
    else:
        flash(f"No se pudieron actualizar los topics de '{nombre}'", "error")

    return redirect("/")


@app.route("/cambia_nombre/<nombre_actual>", methods=["POST"])
def cambia_nombre(nombre_actual):
    validar_nombre(nombre_actual)
    nuevo_nombre = request.form.get("nuevo-nombre")
    validar_nombre(nuevo_nombre)

    respuesta = github_api.renombrar_repo(nombre_actual, nuevo_nombre)

    if respuesta.ok:
        github_api.limpiar_cache()
        flash("Repositorio renombrado correctamente", "success")
    else:
        flash("Ocurrio un error al renombrar el repositorio", "error")

    return redirect("/")


@app.route("/crea_repo", methods=["POST"])
def crea_repo():
    nombre = request.form.get("nombre")
    visibilidad = request.form.get("visibilidad") == "si"
    gitignore = request.form.get("gitignore")

    if not NOMBRE_REPO_RE.match(nombre or ""):
        flash("Debes indicar un nombre de repositorio válido", "error")
        return redirect("/")

    mensaje = git_ops.crear_repo(nombre, visibilidad, gitignore)
    flash(mensaje, "success" if "correctamente" in mensaje else "error")
    return redirect("/")


@app.route("/clona_repo/<nombre>/<visibilidad>", methods=["POST"])
def clona_repo(nombre, visibilidad):
    if visibilidad not in VISIBILIDADES:
        abort(404)
    validar_nombre(nombre)

    mensaje = git_ops.clonar_repo(nombre, visibilidad)
    flash(mensaje, "success" if "correctamente" in mensaje else "error")
    return redirect("/")


@app.route("/clona_repos", methods=["POST"])
def clona_repos():
    mensaje, categoria = git_ops.clonar_todos()
    flash(mensaje, categoria)
    return redirect("/")


@app.route("/estado_repo/<visibilidad>/<nombre>", methods=["GET"])
def estado_repo(visibilidad, nombre):
    carpeta_repo = ruta_repo(visibilidad, nombre)

    if not carpeta_repo.exists():
        return jsonify({
            "error": f"El repositorio {nombre} no existe"
        }), 404

    return {"archivos": git_ops.estado_archivos(carpeta_repo)}


@app.route("/commit_repo/<visibilidad>/<nombre>", methods=["POST"])
def commit_repo(visibilidad, nombre):
    archivos = request.form.getlist("archivos")
    mensaje = request.form.get("mensaje-commit")

    if not archivos:
        flash("Debes seleccionar al menos un archivo", "error")
        return redirect("/")

    carpeta_repo = ruta_repo(visibilidad, nombre)

    if git_ops.hacer_commit(carpeta_repo, archivos, mensaje):
        flash(f"Instantánea creada en {carpeta_repo} con {len(archivos)} archivo(s)", "success")
    else:
        flash(f"Error al crear la instantánea en {carpeta_repo}", "error")

    return redirect("/")


@app.route("/push_repo/<visibilidad>/<nombre>", methods=["POST"])
def push_repo(visibilidad, nombre):
    carpeta_repo = ruta_repo(visibilidad, nombre)

    if git_ops.hacer_push(carpeta_repo):
        flash(f"Repositorio actualizado en {carpeta_repo}", "success")
    else:
        flash(f"Error al actualizar el repositorio en {carpeta_repo}", "error")

    return redirect("/")


@app.route("/cambiar_visibilidad/<nombre>", methods=["POST"])
def cambiar_visibilidad(nombre):
    validar_nombre(nombre)
    privado = request.form.get("cambia-visibilidad") == "on"

    nueva_visibilidad = "privado" if privado else "publico"
    anterior_visibilidad = "publico" if privado else "privado"

    antigua_ruta_repo = CARPETA_REPOS / anterior_visibilidad / nombre
    nueva_ruta_repo = CARPETA_REPOS / nueva_visibilidad / nombre

    respuesta = github_api.cambiar_visibilidad_repo(nombre, privado)

    if respuesta.status_code == 200:
        github_api.limpiar_cache()
        if antigua_ruta_repo.exists():
            shutil.move(antigua_ruta_repo, nueva_ruta_repo)
        flash(f"Cambiada repo '{nombre}' de {anterior_visibilidad} a {nueva_visibilidad}", "success")
        return redirect("/")

    flash(f"No se pudo cambiar repo {nombre} de {anterior_visibilidad} a {nueva_visibilidad}", "error")
    return redirect("/")


@app.route("/crea_elimina_pagina/<nombre>", methods=["POST"])
def crea_elimina_pagina(nombre):
    validar_nombre(nombre)

    estado = github_api.estado_pagina(nombre)

    if estado.status_code == 200:
        respuesta = github_api.eliminar_pagina(nombre)
        if respuesta.status_code == 204:
            github_api.limpiar_cache()
            flash("Página eliminada correctamente", "success")
            return redirect("/")
        flash(f"No se pudo eliminar la página: {respuesta.text}", "error")
        return redirect("/")

    if estado.status_code == 404:
        respuesta = github_api.crear_pagina(nombre)
        if respuesta.status_code in [201, 204]:
            github_api.limpiar_cache()
            flash("Pagina creada correctamente", "success")
            return redirect("/")
        flash("No se ha podido crear la pagina", "error")
        return redirect("/")

    flash(f"Error al consultar el estado de la página: {estado.text}", "error")
    return redirect("/")


@app.route('/elimina_repo/<nombre>', methods=["POST"])
def elimina_repo(nombre):
    validar_nombre(nombre)

    respuesta = github_api.eliminar_repo(nombre)

    if respuesta.status_code != 204:
        flash(f"Error {respuesta.status_code}: {respuesta.json().get('message')}", "error")
        return redirect("/")

    github_api.limpiar_cache()
    flash(f"Repositorio '{nombre}' eliminado correctamente", "success")
    return redirect("/")


@app.route('/crea_tag/<visibilidad>/<nombre>', methods=["POST"])
def crea_tag(visibilidad, nombre):
    mensaje = request.form.get("mensaje-tag")
    version = request.form.get("version-tag")

    carpeta_repo = ruta_repo(visibilidad, nombre)

    if git_ops.crear_tag(carpeta_repo, version, mensaje):
        flash("Repositorio tagueado correctamente", "success")
    else:
        flash("Error al crear o enviar el tag", "error")

    return redirect("/")


if __name__ == "__main__":
    import os
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
