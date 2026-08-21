import base64
import time

import requests

from config import GITHUB_USER, GITHUB_TOKEN

API_GITHUB = "https://api.github.com/user/repos"
GITIGNORE_REPO = "https://api.github.com/repos/github/gitignore/contents"

CABECERAS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# TTL de la caché en memoria para lecturas de la API
CACHE_TTL_SEGUNDOS = 300
_cache = {}


def limpiar_cache():
    _cache.clear()


def _desde_cache(clave):
    entrada = _cache.get(clave)
    if entrada and time.monotonic() - entrada["tiempo"] < CACHE_TTL_SEGUNDOS:
        return entrada["valor"]
    return None


def _a_cache(clave, valor):
    _cache[clave] = {"valor": valor, "tiempo": time.monotonic()}


def url_repo(nombre):
    return f"https://api.github.com/repos/{GITHUB_USER}/{nombre}"


def obtener_repos():
    """Devuelve todos los repositorios del usuario recorriendo la paginación."""
    en_cache = _desde_cache("repos")
    if en_cache is not None:
        return en_cache

    repos = []
    pagina = 1

    while True:
        respuesta = requests.get(
            API_GITHUB,
            headers=CABECERAS,
            params={"per_page": 100, "page": pagina}
        )
        datos = respuesta.json()

        if respuesta.status_code != 200:
            mensaje = datos.get("message", "Error desconocido")
            raise RuntimeError(f"Error {respuesta.status_code}: {mensaje}")

        if not datos:
            break

        repos.extend(datos)
        pagina += 1

    _a_cache("repos", repos)
    return repos


def obtener_templates_gitignore():
    en_cache = _desde_cache("templates_gitignore")
    if en_cache is not None:
        return en_cache

    respuesta = requests.get(GITIGNORE_REPO)
    templates = []

    if respuesta.status_code == 200:
        for archivo in respuesta.json():
            if archivo["name"].endswith(".gitignore"):
                templates.append(archivo["name"].replace(".gitignore", ""))
        _a_cache("templates_gitignore", templates)

    return templates


def descargar_template(template):
    url = f"{GITIGNORE_REPO}/{template}"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        contenido = respuesta.json()["content"]
        return base64.b64decode(contenido).decode()
    return ""


def crear_repo_remoto(nombre, privado):
    datos = {
        "name": nombre,
        "description": f"Proyecto {nombre} subido automáticamente.",
        "private": privado
    }
    return requests.post(API_GITHUB, headers=CABECERAS, json=datos)


def renombrar_repo(nombre_actual, nuevo_nombre):
    return requests.patch(
        url_repo(nombre_actual),
        headers=CABECERAS,
        json={"name": nuevo_nombre},
    )


def cambiar_visibilidad_repo(nombre, privado):
    return requests.patch(url_repo(nombre), headers=CABECERAS, json={"private": privado})


def eliminar_repo(nombre):
    return requests.delete(url_repo(nombre), headers=CABECERAS)


def actualizar_topics(nombre, topics):
    return requests.put(
        f"{url_repo(nombre)}/topics",
        headers=CABECERAS,
        json={"names": topics}
    )


def estado_pagina(nombre):
    return requests.get(f"{url_repo(nombre)}/pages", headers=CABECERAS)


TAMANIO_MAXIMO_ARCHIVO = 512 * 1024


def obtener_contenido(nombre, ruta=""):
    """Devuelve la respuesta de la API de contenidos de GitHub para una ruta del repo."""
    clave = f"contenido:{nombre}:{ruta}"
    en_cache = _desde_cache(clave)
    if en_cache is not None:
        return en_cache

    url = f"{url_repo(nombre)}/contents/{ruta}" if ruta else f"{url_repo(nombre)}/contents"
    respuesta = requests.get(url, headers=CABECERAS)
    _a_cache(clave, respuesta)
    return respuesta


def crear_pagina(nombre):
    datos = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    return requests.post(f"{url_repo(nombre)}/pages", headers=CABECERAS, json=datos)


def eliminar_pagina(nombre):
    return requests.delete(f"{url_repo(nombre)}/pages", headers=CABECERAS)
