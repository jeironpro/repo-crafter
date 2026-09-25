import base64
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


def seleccion_repos():
    """Devuelve la lista de pares (visibilidad, nombre) validados del formulario.

    Cada campo 'seleccionados' codifica un repo como 'visibilidad/nombre',
    lo que permite validar la visibilidad y bloquear inyecciones de ruta.
    """
    pares = []
    for codigo in request.form.getlist("seleccionados"):
        visibilidad, separador, nombre = codigo.partition("/")
        if (
            separador
            and visibilidad in VISIBILIDADES
            and NOMBRE_REPO_RE.match(nombre or "")
        ):
            pares.append((visibilidad, nombre))
    return pares


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
    formato = request.args.get("formato", "pdf")

    if formato not in {"pdf", "docx"}:
        abort(400)

    try:
        repos = github_api.obtener_repos()
    except RuntimeError as error:
        return str(error)

    grupos = resumen.clasificar_repos(repos)
    topics = {repo["name"]: resumen.topics_despliegue(repo) for repo in grupos["desplegados"]}
    topics.update({repo["name"]: resumen.topics_no_autorizado(repo) for repo in grupos["no_autorizado"]})
    topics.update({repo["name"]: resumen.topics_mi_contenido(repo) for repo in grupos["mi_contenido"]})

    lenguajes_por_repo = {}
    for repo in repos:
        try:
            lenguajes_por_repo[repo["name"]] = github_api.obtener_lenguajes(repo["name"])
        except RuntimeError:
            lenguajes_por_repo[repo["name"]] = {}

    lenguajes = resumen.lenguajes_de_repos(lenguajes_por_repo)

    if formato == "docx":
        contenido = resumen.generar_docx(grupos, topics, GITHUB_USER, lenguajes)
        mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        tokens = (Path(app.root_path) / "static" / "css" / "tokens.css").read_text(encoding="utf-8")
        html = render_template(
            "resumen.html",
            grupos=grupos,
            topics=topics,
            lenguajes=lenguajes,
            tokens=tokens,
            usuario=GITHUB_USER,
            fecha=date.today().strftime("%d/%m/%Y"),
            total=len(repos)
        )
        contenido = resumen.generar_pdf(html)
        mimetype = "application/pdf"

    return Response(
        contenido,
        mimetype=mimetype,
        headers={"Content-Disposition": f"attachment; filename={resumen.nombre_archivo(formato)}"}
    )


@app.route("/archivos/<nombre>", methods=["GET"])
def lista_archivos(nombre):
    validar_nombre(nombre)

    relativa = request.args.get("ruta", "").strip("/")
    if ".." in relativa.split("/"):
        abort(404)

    respuesta = github_api.obtener_contenido(nombre, relativa)

    if respuesta.status_code == 200:
        entradas = respuesta.json()
    elif respuesta.status_code == 404 and "empty" in respuesta.json().get("message", "").lower():
        entradas = []
    else:
        abort(404)

    if not isinstance(entradas, list):
        abort(404)

    carpetas = [{"nombre": e["name"]} for e in entradas if e.get("type") == "dir"]
    archivos = [{"nombre": e["name"], "tamano": e.get("size", 0)} for e in entradas if e.get("type") == "file"]

    return {"carpetas": carpetas, "archivos": archivos}


@app.route("/archivo/<nombre>", methods=["GET"])
def ver_archivo(nombre):
    validar_nombre(nombre)

    relativa = request.args.get("ruta", "").strip("/")
    if not relativa or ".." in relativa.split("/"):
        abort(404)

    respuesta = github_api.obtener_contenido(nombre, relativa)

    if respuesta.status_code != 200:
        abort(404)

    datos = respuesta.json()

    if datos.get("type") != "file":
        abort(404)

    if datos.get("size", 0) > github_api.TAMANIO_MAXIMO_ARCHIVO:
        return {"error": "El archivo supera el límite de 512 KB"}, 413

    contenido = base64.b64decode(datos.get("content", ""))

    if b"\0" in contenido[:8192]:
        return {"error": "El archivo no es texto plano"}, 415

    return {
        "nombre": datos.get("name", relativa),
        "contenido": contenido.decode("utf-8", errors="replace")
    }


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


@app.route("/about_repo/<nombre>", methods=["GET"])
def about_repo(nombre):
    validar_nombre(nombre)

    try:
        repos = github_api.obtener_repos()
    except RuntimeError as error:
        return str(error), 503

    repo = next((repo for repo in repos if repo["name"] == nombre), None)

    if repo is None:
        abort(404)

    return {
        "nombre": repo["name"],
        "descripcion": repo.get("description") or "",
        "web": repo.get("homepage") or "",
    }


@app.route("/about/<nombre>", methods=["POST"])
def guarda_about(nombre):
    validar_nombre(nombre)

    descripcion = request.form.get("descripcion-about", "").strip()
    web = request.form.get("web-about", "").strip()

    respuesta = github_api.actualizar_about(nombre, descripcion, web)

    if respuesta.status_code in [200, 204]:
        github_api.limpiar_cache()
        flash(f"About de '{nombre}' actualizado correctamente", "success")
    else:
        flash(f"No se pudo actualizar el about de '{nombre}'", "error")

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


@app.route("/clona_repos_seleccion", methods=["POST"])
def clona_repos_seleccion():
    pares = seleccion_repos()

    if not pares:
        flash("Debes seleccionar al menos un repositorio", "error")
        return redirect("/")

    clonados = 0
    errores = 0

    for visibilidad, nombre in pares:
        mensaje = git_ops.clonar_repo(nombre, visibilidad)
        if "correctamente" in mensaje:
            clonados += 1
        else:
            errores += 1

    if clonados and errores:
        flash(f"{clonados} repositorio(s) clonados y {errores} con errores", "success")
    elif clonados:
        flash(f"{clonados} repositorio(s) clonados correctamente", "success")
    else:
        flash("No se pudo clonar ninguno de los repositorios seleccionados", "error")

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


@app.route("/pull_repo/<visibilidad>/<nombre>", methods=["POST"])
def pull_repo(visibilidad, nombre):
    carpeta_repo = ruta_repo(visibilidad, nombre)

    if not carpeta_repo.exists():
        flash(f"El repositorio local '{nombre}' no existe", "error")
    elif git_ops.hacer_pull(carpeta_repo):
        flash(f"Pull realizado correctamente en '{nombre}'", "success")
    else:
        flash(f"Error al hacer pull en '{nombre}'", "error")

    return redirect("/")


@app.route("/fetch_repo/<visibilidad>/<nombre>", methods=["POST"])
def fetch_repo(visibilidad, nombre):
    carpeta_repo = ruta_repo(visibilidad, nombre)

    if not carpeta_repo.exists():
        flash(f"El repositorio local '{nombre}' no existe", "error")
    elif git_ops.hacer_fetch(carpeta_repo):
        flash(f"Fetch realizado correctamente en '{nombre}'", "success")
    else:
        flash(f"Error al hacer fetch en '{nombre}'", "error")

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


@app.route("/elimina_repos", methods=["POST"])
def elimina_repos():
    pares = seleccion_repos()

    if not pares:
        flash("Debes seleccionar al menos un repositorio", "error")
        return redirect("/")

    eliminados = 0

    for _, nombre in pares:
        if github_api.eliminar_repo(nombre).status_code == 204:
            eliminados += 1

    if eliminados:
        github_api.limpiar_cache()
        flash(f"{eliminados} repositorio(s) eliminados correctamente", "success")
    else:
        flash("No se pudo eliminar ninguno de los repositorios seleccionados", "error")

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
