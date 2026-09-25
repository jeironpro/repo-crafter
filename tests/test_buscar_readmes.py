import base64
import csv

import pytest

from buscar_readmes import CSV_DEFECTO, guardar_csv, normalizar, contiene_texto_buscado, obtener_readme


def test_normalizar_ignora_saltos_de_linea_markdown():
    texto = "Linea uno.  \r\nLinea dos\r\n"
    assert normalizar(texto) == "Linea uno.\nLinea dos\n"


def test_contiene_texto_buscado_con_plantilla_exacta():
    readme = (
        "# mi-proyecto\n\n"
        "## 📌 Descripción\n"
        "Este proyecto forma parte de mi portafolio personal.  \n"
        "El objetivo es demostrar buenas prácticas de programación, organización y documentación en GitHub.\n"
        "\n## 📜 Licencia\n"
    )
    assert contiene_texto_buscado(readme)


def test_contiene_texto_buscado_sin_doble_espacio():
    readme = (
        "## 📌 Descripción\n"
        "Este proyecto forma parte de mi portafolio personal.\n"
        "El objetivo es demostrar buenas prácticas de programación, organización y documentación en GitHub.\n"
    )
    assert contiene_texto_buscado(readme)


def test_no_contiene_texto_buscado():
    readme = "# Otro proyecto\n\n## Descripción\nUn proyecto distinto.\n"
    assert not contiene_texto_buscado(readme)


class RespuestaReadmeFake:
    def __init__(self, contenido=None, status_code=200):
        self.contenido = contenido
        self.status_code = status_code
        self.headers = {"content-type": "application/json"}

    def json(self):
        if self.status_code == 404:
            return {"message": "Not Found"}
        return {"content": base64.b64encode(self.contenido.encode()).decode()}


def test_obtener_readme_devuelve_contenido(monkeypatch):
    contenido = "# Repo\n\nHola"
    respuesta = RespuestaReadmeFake(contenido=contenido)

    def fake_get(url, headers):
        assert url == "https://api.github.com/repos/usuario-test/repo-uno/readme"
        return respuesta

    monkeypatch.setattr("buscar_readmes.requests.get", fake_get)
    assert obtener_readme("repo-uno") == contenido


def test_obtener_readme_devuelve_none_sin_readme(monkeypatch):
    monkeypatch.setattr(
        "buscar_readmes.requests.get",
        lambda url, headers: RespuestaReadmeFake(status_code=404),
    )
    assert obtener_readme("repo-uno") is None


def test_obtener_readme_lanza_error_con_api_fallida(monkeypatch):
    respuesta = RespuestaReadmeFake(status_code=500)
    respuesta.headers = {"content-type": "application/json"}

    def fake_get(url, headers):
        respuesta.json = lambda: {"message": "Internal Server Error"}
        return respuesta

    monkeypatch.setattr("buscar_readmes.requests.get", fake_get)
    with pytest.raises(RuntimeError, match="Error 500"):
        obtener_readme("repo-uno")


def test_guardar_csv_escribe_nombre_visibilidad_y_url(tmp_path):
    ruta = tmp_path / "coincidencias.csv"
    coincidencias = [
        {"nombre": "repo-uno", "visibilidad": "público", "url": "https://github.com/usuario-test/repo-uno"},
        {"nombre": "repo-dos", "visibilidad": "privado", "url": "https://github.com/usuario-test/repo-dos"},
    ]

    guardar_csv(coincidencias, ruta)

    with open(ruta, newline="", encoding="utf-8-sig") as archivo:
        filas = list(csv.DictReader(archivo))

    assert filas == coincidencias


def test_guardar_csv_con_lista_vacia_solo_escribe_cabecera(tmp_path):
    ruta = tmp_path / "vacio.csv"

    guardar_csv([], ruta)

    with open(ruta, newline="", encoding="utf-8-sig") as archivo:
        filas = list(csv.DictReader(archivo))

    assert filas == []
    with open(ruta, encoding="utf-8-sig") as archivo:
        assert archivo.read().startswith("nombre,visibilidad,url")


def test_csv_por_defecto_tiene_nombre_fijo():
    assert CSV_DEFECTO == "coincidencias-portafolio.csv"