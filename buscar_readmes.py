"""Script externo: busca en los README de todos los repositorios de GitHub.

Recorre todos los repositorios del usuario (vía API de GitHub) y muestra
aquellos cuyo README.md contiene el texto de la plantilla del portafolio:

    ## 📌 Descripción
    Este proyecto forma parte de mi portafolio personal.
    El objetivo es demostrar buenas prácticas de programación, organización y
    documentación en GitHub.

Uso:
    python buscar_readmes.py [--csv [RUTA]]

Con --csv se exportan las coincidencias a un archivo CSV (nombre, visibilidad,
URL). La ruta es opcional; por defecto se crea 'coincidencias-portafolio.csv'.

Requisitos: variables GITHUB_USER y GITHUB_TOKEN en el archivo .env
(las mismas que usa la aplicación).
"""
import argparse
import base64
import csv

import requests

from config import GITHUB_USER, GITHUB_TOKEN
from github_api import CABECERAS, url_repo, obtener_repos

# Nombre por defecto del CSV de resultados
CSV_DEFECTO = "coincidencias-portafolio.csv"

# Texto buscado en los README (misma plantilla que usa git_ops.crear_repo)
TEXTO_BUSCADO = """## 📌 Descripción"""


def normalizar(texto):
    """Normaliza saltos de línea (CRLF/CR) y espacios finales de cada línea.

    Así un README con el salto de línea Markdown (dos espacios finales) o
    guardado con finales de línea de Windows sigue considerándose igual.
    """
    lineas = texto.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return "\n".join(linea.rstrip() for linea in lineas)


def contiene_texto_buscado(readme):
    """Devuelve True si el contenido del README contiene el texto buscado."""
    return normalizar(TEXTO_BUSCADO) in normalizar(readme)


def obtener_readme(nombre):
    """Devuelve el texto del README.md del repositorio, o None si no tiene."""
    respuesta = requests.get(f"{url_repo(nombre)}/readme", headers=CABECERAS)

    if respuesta.status_code == 404:
        return None

    if respuesta.status_code != 200:
        mensaje = respuesta.json().get("message", "Error desconocido") if respuesta.headers.get("content-type", "").startswith("application/json") else respuesta.text
        raise RuntimeError(f"Error {respuesta.status_code} al leer el README de '{nombre}': {mensaje}")

    datos = respuesta.json()
    if isinstance(datos, dict) and "content" in datos:
        return base64.b64decode(datos["content"]).decode("utf-8")
    return respuesta.text


def guardar_csv(coincidencias, ruta):
    """Escribe las coincidencias (nombre, visibilidad, url) en un archivo CSV.

    Se usa utf-8-sig (BOM) para que Excel muestre bien los acentos.
    """
    with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["nombre", "visibilidad", "url"])
        escritor.writeheader()
        escritor.writerows(coincidencias)


def main():
    analizador = argparse.ArgumentParser(
        description="Busca en los README de todos los repositorios el texto del portafolio."
    )
    analizador.add_argument(
        "--csv",
        nargs="?",
        const=CSV_DEFECTO,
        metavar="RUTA",
        help=f"Exporta las coincidencias a un CSV (ruta opcional; por defecto '{CSV_DEFECTO}').",
    )
    argumentos = analizador.parse_args()

    if not GITHUB_USER or not GITHUB_TOKEN:
        print("Error: faltan GITHUB_USER y/o GITHUB_TOKEN en el archivo .env")
        return

    repos = obtener_repos()

    if not repos:
        print("No se encontraron repositorios.")
        return

    coincidencias = []

    for repo in repos:
        nombre = repo["name"]
        readme = obtener_readme(nombre)

        if readme is not None and contiene_texto_buscado(readme):
            visibilidad = "privado" if repo["private"] else "público"
            coincidencias.append({
                "nombre": nombre,
                "visibilidad": visibilidad,
                "url": repo["html_url"],
            })
            print(f"- {nombre} ({visibilidad})")

    if coincidencias:
        print(f"\nSe encontraron {len(coincidencias)} repositorio(s) con el texto del portafolio.")
        if argumentos.csv:
            guardar_csv(coincidencias, argumentos.csv)
            print(f"Resultados exportados a '{argumentos.csv}'.")
    else:
        print("No se encontraron repositorios con el texto buscado.")


if __name__ == "__main__":
    main()
