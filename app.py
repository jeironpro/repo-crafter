import os
import secrets
import requests
import subprocess
import base64
from flask import Flask, render_template, redirect, flash, request
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

load_dotenv()

GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_EMAIL= os.getenv("GITHUB_EMAIL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITIGNORE_REPO = "https://api.github.com/repos/github/gitignore/contents"

API_GITHUB="https://api.github.com/user/repos"
CABECERAS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}
HOME = Path.home()
CARPETA_REPOS = HOME / "Documentos" / "repositorios"

# Año actual para la licencia
YEAR = datetime.now().year

# Plantilla mínima de README
README_TEMPLATE = """# {project_name}

## 📌 Descripción
Este proyecto forma parte de mi portafolio personal.  
El objetivo es demostrar buenas prácticas de programación, organización y documentación en GitHub.

## 📜 Licencia
Este proyecto está bajo la licencia **MIT**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.
"""

# Plantilla de licencia MIT
LICENSE_TEMPLATE = """MIT License

Copyright (c) {year} {user}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

def obtener_templates_gitignore():
    respuesta = requests.get(GITIGNORE_REPO)
    templates = []

    if respuesta.status_code == 200:
        for archivo in respuesta.json():
            if archivo["name"].endswith(".gitignore"):
                templates.append(archivo["name"].replace(".gitignore", ""))
    return templates

def descargar_template(template):
    url = f"{GITIGNORE_REPO}/{template}"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        contenido = respuesta.json()["content"]
        return base64.b64decode(contenido).decode()
    return ""

def auxiliar_crea_repo(nombre, visibilidad, gitignore):
    sesion = requests.Session()
    sesion.auth = (GITHUB_USER, GITHUB_TOKEN)

    carpeta_repo = CARPETA_REPOS / ("privado" if visibilidad else "publico") / nombre

    if carpeta_repo.exists():
        return f"❌ La carpeta '{carpeta_repo}' ya existe localmente." 
    
    os.makedirs(carpeta_repo, exist_ok=True)

    ruta_readme = carpeta_repo / "README.md"
    with open(ruta_readme, "w", encoding="utf-8") as fichero:
        fichero.write(README_TEMPLATE.format(project_name=nombre))

    ruta_license = carpeta_repo / "LICENSE"
    with open(ruta_license, "w", encoding="utf-8") as fichero:
        fichero.write(LICENSE_TEMPLATE.format(year=YEAR, user=GITHUB_USER))

    ruta_gitignore = carpeta_repo / ".gitignore"

    if gitignore:
        nombre_gitignore = f"{gitignore}.gitignore"
        contenido_gitignore = descargar_template(nombre_gitignore)

        if contenido_gitignore:
            with open(ruta_gitignore, "w", encoding="utf-8") as fichero:
                fichero.write(contenido_gitignore)
        else:
            print(f"⚠️ No se pudo descargar el template '{gitignore}'. Se omitirá el .gitignore.")

    subprocess.run(["git", "-C", str(carpeta_repo), "init"], check=True)

    subprocess.run(["git", "-C", str(carpeta_repo), "branch", "-M", "main"], check=True)

    archivos = ["LICENSE", "README.md"]

    if gitignore and ruta_gitignore.exists():
        archivos.append(".gitignore")

    subprocess.run(["git", "-C", str(carpeta_repo), "add", *archivos], check=True)

    subprocess.run([
        "git", 
        "-C", str(carpeta_repo),
        "-c", f"user.name={GITHUB_USER}",
        "-c", f"user.email={GITHUB_EMAIL}",
        "commit", "-m", "Creando estructura inicial"
        ], check=True
    )

    datos = {
        "name": nombre,
        "description": f"Proyecto {nombre} subido automáticamente.",
        "private": visibilidad
    }

    respuesta = sesion.post(API_GITHUB, json=datos)

    if respuesta.status_code in [201, 422]:
        subprocess.run(["git", "-C", str(carpeta_repo), "remote", "remove", "origin"], check=False, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "-C", str(carpeta_repo), "remote", "add", "origin", f"git@github.com-personal:{GITHUB_USER}/{nombre}.git"], check=True)
        subprocess.run(["git", "-C", str(carpeta_repo), "push", "-u", "origin", "main"], check=True)
        return f"✅ Repositorio '{nombre}' creado y subido correctamente."
    else:
        return f"❌ Error creando repo en GitHub: {respuesta.status_code} {respuesta.text}"

def auxiliar_clona_repo(nombre, visibilidad):
    carpeta_repo = CARPETA_REPOS / visibilidad / nombre
    url_clona = f"git@github.com:{GITHUB_USER}/{nombre}.git"
    
    try:
        subprocess.run(["git", "clone", url_clona, carpeta_repo], check=True)
        return f"Repositorio '{nombre}' clonado en {carpeta_repo} ✅"
    except subprocess.CalledProcessError:
        return f"Error al clona '{nombre}' ❌"

def auxiliar_clona_repos():
    pagina = 1

    while True:
        enlace_clona = f"{API_GITHUB}?per_page=100&page={pagina}"

        respuesta = requests.get(enlace_clona, auth=(GITHUB_USER, GITHUB_TOKEN))

        if respuesta.status_code != 200:
            return f"Error: {respuesta.status_code}, {respuesta.text}", "error"

        repos = respuesta.json()

        if not repos:
            break

        for repo in repos:
            enlace_ssh = repo["ssh_url"]
            nombre = repo["name"]
            visibilidad = repo["private"]

            carpeta_repo = CARPETA_REPOS / ("privado" if visibilidad else "publico") / nombre

            if not carpeta_repo.exists():
                subprocess.run(["git", "clone", enlace_ssh, str(carpeta_repo)], check=True)

        pagina += 1
    return f"Todos los repositorios han sido clonados en {CARPETA_REPOS} ✅"

@app.route('/', methods=["GET", "POST"])
def index():
    parametros = {"per_page": 100}
    repos = []
    pagina = 1
    contador_repo_privados = 0
    contador_repo_publicos = 0
    contador_paginas_creadas = 0

    while True:
        parametros["page"] = pagina
        respuesta = requests.get(API_GITHUB, headers=CABECERAS, params=parametros)
        datos = respuesta.json()

        if respuesta.status_code != 200:
            return f"Error {respuesta.status_code}: {datos.get('message', 'Error desconocido')}"

        if not datos:
            break

        repos.extend(datos)
        pagina += 1

    templetes_gitignore = obtener_templates_gitignore()

    for repo in repos:
        if repo["has_pages"]:
            contador_paginas_creadas += 1
        if repo["private"]:
            contador_repo_privados += 1
        else:
            contador_repo_publicos += 1


    return render_template(
        "index.html", 
        repos=repos, 
        repos_publicos=contador_repo_publicos, 
        paginas_creadas=contador_paginas_creadas, 
        repos_privados=contador_repo_privados, 
        templetes_gitignore=templetes_gitignore
    )

@app.route("/crea_repo", methods=["POST"])
def crea_repo():
    nombre = request.form.get("nombre")
    visibilidad = request.form.get("visibilidad") == "si"
    gitignore = request.form.get("gitignore")

    mensaje = auxiliar_crea_repo(nombre, visibilidad, gitignore)
    flash(mensaje, "success" if "✅" in mensaje else "error")
    return redirect("/")

@app.route("/clona_repo/<nombre>/<visibilidad>", methods=["POST"])
def clona_repo(nombre, visibilidad):
    mensaje = auxiliar_clona_repo(nombre, visibilidad)
    flash(mensaje, "success" if "✅" in mensaje else "error")
    return redirect("/")

@app.route("/clona_repos", methods=["POST"])
def clona_repos():
    mensaje = auxiliar_clona_repos()
    flash(mensaje, "success" if "✅" in mensaje else "error")
    return redirect("/")

@app.route("/estado_repo/<visibilidad>/<nombre>", methods=["GET"])
def estado_repo(visibilidad, nombre):
    carpeta_repo = CARPETA_REPOS / visibilidad  / nombre

    if not carpeta_repo.exists():
        flash(f"El repositorio {carpeta_repo} no existe.", "error")
        return redirect("/")
    
    resultado = subprocess.run(
        ["git", "-C", str(carpeta_repo), "status", "--porcelain"],
        capture_output=True, text=True
    )

    archivos = []
    for linea in resultado.stdout.strip().split("\n"):
        if linea:
            estado = linea[:2].strip()
            archivo = linea[2:].strip()
            archivos.append({"estado": estado, "archivo": archivo})
    
    return {"archivos": archivos}

@app.route("/commit_repo/<visibilidad>/<nombre>", methods=["POST"])
def commit_repo(visibilidad, nombre):
        archivos = request.form.getlist("archivos")
        mensaje = request.form.get("mensaje-commit")

        if not archivos:
            flash("Debes seleccionar al menos un archivo", "error")
            return redirect("/")
        
        carpeta_repo = CARPETA_REPOS / visibilidad / nombre
 
        subprocess.run(["git", "-C", str(carpeta_repo), "add", *archivos])
        subprocess.run([
            "git", 
            "-C", str(carpeta_repo), 
            "-c", f"user.name={GITHUB_USER}",
            "-c", f"user.email={GITHUB_EMAIL}",
            "commit", "-m", mensaje
        ])
        subprocess.run(["git", "-C", str(carpeta_repo), "push", "origin", "main"])

        flash(f"Repositorio actualizado en {carpeta_repo} con {len(archivos)} archivo(s)", "success")
        return redirect("/")

@app.route("/cambiar_visibilidad/<nombre>", methods=["POST"])
def cambiar_visibilidad(nombre):
    visibilidad = request.form.get("cambia-visibilidad")

    nueva_visibilidad = "privado" if visibilidad else "publico"
    anterior_visibilidad = "publico" if nueva_visibilidad == "privado" else "privado"

    antigua_ruta_repo = CARPETA_REPOS / anterior_visibilidad / nombre
    nueva_ruta_repo = CARPETA_REPOS / nueva_visibilidad / nombre

    url_repo = f"https://api.github.com/repos/{GITHUB_USER}/{nombre}"

    datos = {
        "private": visibilidad
    }

    respuesta = requests.patch(url_repo, headers=CABECERAS, json=datos)
    
    if respuesta.status_code == 200:
        subprocess.run(["mv", antigua_ruta_repo, nueva_ruta_repo])
        flash(f"Cambiada repo '{nombre}' de {anterior_visibilidad} a {nueva_visibilidad}", "success")
        return redirect("/")
    
    flash(f"No se pudo cambiar repo {nombre} de {anterior_visibilidad} a {nueva_visibilidad}", "error")
    return redirect("/")

@app.route("/crea_elimina_pagina/<nombre>", methods=["POST"])
def crea_elimina_pagina(nombre):
    url_repo = f"https://api.github.com/repos/{GITHUB_USER}/{nombre}/pages"

    estado = requests.get(url_repo, headers=CABECERAS)

    if estado.status_code == 200:
        respuesta = requests.delete(url_repo, headers=CABECERAS)
        if respuesta.status_code == 204:
            flash("Página eliminada correctamente", "success")
            return redirect("/")
        else:
            flash(f"No se pudo eliminar la página: {respuesta.text}", "error")
            return redirect("/")
    elif estado.status_code == 404:
        datos = {
            "source": {
                "branch": "main",
                "path": "/"
            }
        }

        respuesta = requests.post(url_repo, headers=CABECERAS, json=datos)

        if respuesta.status_code in [201, 204]:
            flash("Pagina creada correctamente", "success")
            return redirect("/")
        else:
            flash("No se ha podido crear la pagina", "error")
            return redirect("/")
    flash(f"Error al consultar el estado de la página: {estado.text}", "error")
    return redirect("/")

@app.route('/elimina_repo/<nombre>', methods=["POST"])
def elimina_repo(nombre):
    url_elimina = f"https://api.github.com/repos/{GITHUB_USER}/{nombre}"
    respuesta = requests.delete(url_elimina, headers=CABECERAS)

    if respuesta.status_code != 204:
        flash(f"Error {respuesta.status_code}: {respuesta.json().get('message')}")
        return redirect("/")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)