import base64
from unittest.mock import patch

from tests.conftest import RespuestaFake


def get_falso(url, **kwargs):
    if "/repos/usuario-test/repo-vacio/" in url:
        return RespuestaFake(status_code=404, datos={"message": "This repository is empty."})
    if url.endswith("/contents"):
        return RespuestaFake(datos=[
            {"name": "src", "type": "dir", "size": 0},
            {"name": "README.md", "type": "file", "size": 120},
            {"name": ".gitignore", "type": "file", "size": 40},
        ])
    if url.endswith("/contents/src"):
        return RespuestaFake(datos=[{"name": "main.py", "type": "file", "size": 20}])
    if url.endswith("/contents/README.md"):
        return RespuestaFake(datos={
            "name": "README.md", "type": "file", "size": 7,
            "encoding": "base64",
            "content": base64.b64encode("# Hola\n".encode()).decode(),
        })
    if url.endswith("/contents/binario.bin"):
        return RespuestaFake(datos={
            "name": "binario.bin", "type": "file", "size": 4,
            "encoding": "base64",
            "content": base64.b64encode(b"\0\1\2\3").decode(),
        })
    if url.endswith("/contents/grande.txt"):
        return RespuestaFake(datos={
            "name": "grande.txt", "type": "file",
            "size": 512 * 1024 + 1,
            "encoding": "base64",
            "content": "",
        })
    if url.endswith("/contents/fantasma.md"):
        return RespuestaFake(status_code=404, datos={"message": "Not Found"})
    return RespuestaFake(status_code=404, datos={"message": "Not Found"})


def test_lista_archivos_separa_carpetas_y_archivos(cliente):
    with patch("github_api.requests.get", side_effect=get_falso):
        respuesta = cliente.get("/archivos/repo-uno")

    assert respuesta.status_code == 200
    datos = respuesta.json
    assert datos["carpetas"] == [{"nombre": "src"}]
    assert [a["nombre"] for a in datos["archivos"]] == ["README.md", ".gitignore"]


def test_lista_archivos_de_subcarpeta(cliente):
    with patch("github_api.requests.get", side_effect=get_falso):
        respuesta = cliente.get("/archivos/repo-uno?ruta=src")

    assert respuesta.status_code == 200
    assert respuesta.json["archivos"] == [{"nombre": "main.py", "tamano": 20}]


def test_lista_archivos_repo_vacio_devuelve_listas_vacias(cliente):
    with patch("github_api.requests.get", side_effect=get_falso):
        respuesta = cliente.get("/archivos/repo-vacio")

    assert respuesta.status_code == 200
    assert respuesta.json == {"carpetas": [], "archivos": []}


def test_lista_archivos_rechaza_traversal(cliente):
    with patch("github_api.requests.get", side_effect=get_falso):
        assert cliente.get("/archivos/repo-uno?ruta=../otro").status_code == 404


def test_lista_archivos_rechaza_nombre_invalido(cliente):
    assert cliente.get("/archivos/nombre%20invalido").status_code == 404


def test_ver_archivo_texto_devuelve_contenido_decodificado(cliente):
    with patch("github_api.requests.get", side_effect=get_falso):
        respuesta = cliente.get("/archivo/repo-uno?ruta=README.md")

    assert respuesta.status_code == 200
    assert respuesta.json == {"nombre": "README.md", "contenido": "# Hola\n"}


def test_ver_archivo_binario_devuelve_415(cliente):
    with patch("github_api.requests.get", side_effect=get_falso):
        respuesta = cliente.get("/archivo/repo-uno?ruta=binario.bin")

    assert respuesta.status_code == 415
    assert "texto plano" in respuesta.json["error"]


def test_ver_archivo_grande_devuelve_413(cliente):
    with patch("github_api.requests.get", side_effect=get_falso):
        respuesta = cliente.get("/archivo/repo-uno?ruta=grande.txt")

    assert respuesta.status_code == 413
    assert "512 KB" in respuesta.json["error"]


def test_ver_archivo_inexistente_devuelve_404(cliente):
    with patch("github_api.requests.get", side_effect=get_falso):
        assert cliente.get("/archivo/repo-uno?ruta=fantasma.md").status_code == 404


def test_ver_archivo_sin_ruta_rechaza(cliente):
    assert cliente.get("/archivo/repo-uno").status_code == 404
