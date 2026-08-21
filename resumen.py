"""Clasificación de repositorios y generación del PDF resumen.

Un repo se considera desplegado cuando algún topic contiene "pages"
(p. ej. github-pages, cloudflare-pages, cf-pages).
"""
from datetime import date

from weasyprint import HTML

TOPIC_DESPLIEGUE = "pages"


def topics_despliegue(repo):
    return [topic for topic in repo.get("topics", []) if TOPIC_DESPLIEGUE in topic.lower()]


def esta_desplegado(repo):
    return bool(topics_despliegue(repo))


def clasificar_repos(repos):
    grupos = {"desplegados": [], "publicos": [], "privados": []}

    for repo in repos:
        if esta_desplegado(repo):
            grupos["desplegados"].append(repo)
        elif repo["private"]:
            grupos["privados"].append(repo)
        else:
            grupos["publicos"].append(repo)

    for lista in grupos.values():
        lista.sort(key=lambda repo: repo["name"].lower())

    return grupos


def nombre_archivo():
    return f"resumen-repos-{date.today().isoformat()}.pdf"


def generar_pdf(html):
    return HTML(string=html).write_pdf()
