import os
import secrets
import requests
import subprocess
from flask import Flask, render_template, redirect, flash, request
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

load_dotenv()

USER = os.getenv("USER")
TOKEN = os.getenv("TOKEN")
API_GITHUB="https://api.github.com/user/repos"
CABECERAS = {
    "Authorization": f"token {TOKEN}",
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

Copyright (c) {year} {USER}

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

def auxiliar_crea_repo(nombre, visibilidad):
    sesion = requests.Session()
    sesion.auth = (USER, TOKEN)

    carpeta_repo = CARPETA_REPOS / ("privado" if visibilidad else "publico") / nombre

    if carpeta_repo.exists():
        return f"❌ La carpeta '{nombre}' ya existe localmente." 
    
    os.makedirs(carpeta_repo, exist_ok=True)

    ruta_readme = carpeta_repo / "README.md"
    with open(ruta_readme, "w", encoding="utf-8") as fitxer:
        fitxer.write(README_TEMPLATE.format(project_name=nombre))

    ruta_license = carpeta_repo / "LICENSE"
    with open(ruta_license, "w", encoding="utf-8") as fitxer:
        fitxer.write(LICENSE_TEMPLATE.format(year=YEAR, USER=USER))

    os.chdir(carpeta_repo)
    subprocess.run(["git", "init"])
    subprocess.run(["git", "branch", "-M", "main"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Agregando README & LICENSE"], stderr=subprocess.DEVNULL)

    datos = {
        "name": nombre,
        "description": f"Proyecto {nombre} subido automáticamente.",
        "private": visibilidad
    }

    respuesta = sesion.post(API_GITHUB, json=datos)

    if respuesta.status_code in [201, 422]:
        subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.DEVNULL)
        subprocess.run(["git", "remote", "add", "origin", f"git@github.com:{USER}/{nombre}.git"])
        subprocess.run(["git", "push", "-u", "origin", "main", "--force"])
        return f"✅ Repositorio '{nombre}' creado y subido correctamente."
    else:
        return f"❌ Error creando repo en GitHub: {respuesta.status_code} {respuesta.text}"

def auxliar_clona_repo(nombre, visibilidad):
    carpeta_repo = CARPETA_REPOS / visibilidad / nombre
    url_clona = f"https://{TOKEN}@github.com/{USER}/{nombre}.git"
    
    try:
        subprocess.run(["git", "clone", url_clona, carpeta_repo], check=True)
        return f"Repositorio '{nombre}' clonado en {carpeta_repo} ✅"
    except subprocess.CalledProcessError:
        return f"Error al clona '{nombre}' ❌"

@app.route('/', methods=["GET", "POST"])
def index():
    parametros = {"per_page": 100}
    repos = []
    pagina = 1

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

    return render_template("index.html", repos=repos)

@app.route("/crea_repo", methods=["POST"])
def crea_repo():
    print("Entra aqui")
    nombre = request.form.get("nombre")
    visibilidad = request.form.get("visibilidad") == "si"

    print(nombre)
    print(visibilidad)

    mensaje = auxiliar_crea_repo(nombre, visibilidad)
    print(mensaje)
    flash("mensaje", "success" if "✅" in mensaje else "error")
    return redirect("/")

@app.route("/clona_repo/<nombre>/<visibilidad>", methods=["POST"])
def clona_repo(nombre, visibilidad):
    mensaje = auxliar_clona_repo(nombre, visibilidad)
    flash(mensaje, "success" if "✅" in mensaje else "error")
    return redirect("/")

@app.route('/elimina_repo/<nombre>', methods=["POST"])
def elimina_repo(nombre):
    url_elimina = f"https://api.github.com/repos/{USER}/{nombre}"
    respuesta = requests.delete(url_elimina, headers=CABECERAS)

    if respuesta.status_code != 204:
        flash(f"Error {respuesta.status_code}: {respuesta.json().get('message')}")
        return redirect("/")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)