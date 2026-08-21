from unittest.mock import patch

import pytest
from werkzeug.exceptions import NotFound

import github_api
from app import ruta_repo


def test_index_muestra_repos_y_estadisticas(cliente, repo_falso, respuesta_fake):
    repos = [
        repo_falso("publico-uno", topics=["flask"]),
        repo_falso("privado-uno", privado=True),
        repo_falso("con-paginas", paginas=True),
    ]

    def get_falso(url, **kwargs):
        if url.startswith("https://api.github.com/user/repos"):
            pagina = kwargs["params"].get("page", 1)
            return respuesta_fake(datos=repos if pagina == 1 else [])
        if "gitignore" in url:
            return respuesta_fake(datos=[{"name": "Python.gitignore"}, {"name": "README.md"}])
        return respuesta_fake(status_code=404, texto="no encontrado")

    with patch("github_api.requests.get", side_effect=get_falso):
        respuesta = cliente.get("/")

    assert respuesta.status_code == 200
    cuerpo = respuesta.data.decode()
    assert "publico-uno" in cuerpo
    assert "privado-uno" in cuerpo
    assert "Python" in cuerpo


def test_ruta_repo_rechaza_traversal():
    with pytest.raises(NotFound):
        ruta_repo("../../etc", "passwd")

    with pytest.raises(NotFound):
        ruta_repo("publico", "../escape")


def test_estado_repo_valida_parametros(cliente):
    assert cliente.get("/estado_repo/inexistente/repo-uno").status_code == 404
    assert cliente.get("/estado_repo/publico/nombre%20invalido").status_code == 404


def test_cambiar_visibilidad_envia_booleano(cliente, respuesta_fake):
    with patch("github_api.requests.patch", return_value=respuesta_fake(status_code=200)) as patch_mock, \
         patch("app.shutil.move"):
        cliente.post("/cambiar_visibilidad/repo-uno", data={"cambia-visibilidad": "on"})
        _, kwargs = patch_mock.call_args
        assert kwargs["json"] == {"private": True}

        cliente.post("/cambiar_visibilidad/repo-uno", data={})
        _, kwargs = patch_mock.call_args
        assert kwargs["json"] == {"private": False}


def test_cambia_nombre_rechaza_nombre_invalido(cliente):
    respuesta = cliente.post("/cambia_nombre/repo-uno", data={"nuevo-nombre": "../malo"})
    assert respuesta.status_code == 404


def test_elimina_repo_exito_y_error(cliente, respuesta_fake, flashes):
    with patch("github_api.requests.delete", return_value=respuesta_fake(status_code=204)):
        respuesta = cliente.post("/elimina_repo/repo-uno")
    assert respuesta.status_code == 302
    assert flashes()[-1] == ("success", "Repositorio 'repo-uno' eliminado correctamente")

    error = respuesta_fake(datos={"message": "prohibido"}, status_code=403)
    with patch("github_api.requests.delete", return_value=error):
        cliente.post("/elimina_repo/repo-uno")
    assert flashes()[-1][0] == "error"
    assert "prohibido" in flashes()[-1][1]


def test_commit_repo_exige_archivos(cliente, flashes):
    respuesta = cliente.post("/commit_repo/publico/repo-uno", data={})
    assert respuesta.status_code == 302
    assert flashes()[-1] == ("error", "Debes seleccionar al menos un archivo")


def test_push_repo_reporta_error(cliente, flashes):
    with patch("git_ops.subprocess.run") as run_mock:
        run_mock.return_value.returncode = 1
        respuesta = cliente.post("/push_repo/publico/repo-uno")

    assert respuesta.status_code == 302
    categoria, mensaje = flashes()[-1]
    assert categoria == "error"
    assert "Error al actualizar" in mensaje


def test_crea_tag_comprueba_resultados(cliente, flashes):
    with patch("git_ops.subprocess.run") as run_mock:
        run_mock.return_value.returncode = 0
        datos = {"version-tag": "v1.0", "mensaje-tag": "release"}
        respuesta = cliente.post("/crea_tag/publico/repo-uno", data=datos)
        assert respuesta.status_code == 302
        assert flashes()[-1][0] == "success"

        run_mock.return_value.returncode = 1
        cliente.post("/crea_tag/publico/repo-uno", data=datos)
        assert flashes()[-1] == ("error", "Error al crear o enviar el tag")


def test_obtener_repos_y_templates_usan_cache(respuesta_fake):
    llamadas = []

    def get_falso(url, **kwargs):
        llamadas.append(url)
        if url.startswith("https://api.github.com/user/repos"):
            pagina = kwargs["params"].get("page", 1)
            return respuesta_fake(datos=[{"name": "uno"}] if pagina == 1 else [])
        return respuesta_fake(datos=[{"name": "Python.gitignore"}])

    with patch("github_api.requests.get", side_effect=get_falso):
        assert len(github_api.obtener_repos()) == 1
        assert github_api.obtener_templates_gitignore() == ["Python"]
        assert len(llamadas) == 3

        github_api.obtener_repos()
        github_api.obtener_templates_gitignore()
        assert len(llamadas) == 3


def test_limpiar_cache_fuerza_nuevas_peticiones(respuesta_fake):
    llamadas = []

    def get_falso(url, **kwargs):
        llamadas.append(url)
        return respuesta_fake(datos=[{"name": "Python.gitignore"}])

    with patch("github_api.requests.get", side_effect=get_falso):
        github_api.obtener_templates_gitignore()
        github_api.limpiar_cache()
        github_api.obtener_templates_gitignore()

    assert len(llamadas) == 2
