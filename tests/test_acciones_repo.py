from unittest.mock import patch

import pytest

import git_ops


def test_about_repo_devuelve_descripcion_y_web(cliente, repo_falso, respuesta_fake):
    repo = repo_falso(nombre="repo-uno")
    repo["description"] = "Mi portafolio"
    repo["homepage"] = "https://ejemplo.com"

    def obtener_falso():
        return [repo]

    with patch("app.github_api.obtener_repos", side_effect=obtener_falso):
        datos = cliente.get("/about_repo/repo-uno").get_json()

    assert datos == {
        "nombre": "repo-uno",
        "descripcion": "Mi portafolio",
        "web": "https://ejemplo.com",
    }


def test_about_repo_sin_descripcion_devuelve_vacio(cliente, repo_falso):
    with patch("app.github_api.obtener_repos", return_value=[repo_falso("repo-uno")]):
        assert cliente.get("/about_repo/repo-uno").get_json()["descripcion"] == ""


def test_about_repo_rechaza_nombre_invalido(cliente, repo_falso):
    with patch("app.github_api.obtener_repos", return_value=[repo_falso("repo-uno")]):
        assert cliente.get("/about_repo/nombre%20invalido").status_code == 404
        assert cliente.get("/about_repo/../escape").status_code == 404
        assert cliente.get("/about_repo/desconocido").status_code == 404


def test_guarda_about_envia_descripcion_y_web(cliente, respuesta_fake):
    with patch("github_api.requests.patch", return_value=respuesta_fake(status_code=200)) as patch_mock, \
         patch("github_api.limpiar_cache") as limpiar_mock:
        cliente.post(
            "/about/repo-uno",
            data={"descripcion-about": "Mi portafolio", "web-about": "https://ejemplo.com"},
        )

        _, kwargs = patch_mock.call_args
        assert kwargs["json"] == {
            "description": "Mi portafolio",
            "homepage": "https://ejemplo.com",
        }
        limpiar_mock.assert_called_once()


def test_guarda_about_error(cliente, respuesta_fake, flashes):
    with patch("github_api.requests.patch", return_value=respuesta_fake(status_code=422)):
        cliente.post("/about/repo-uno", data={"descripcion-about": "Hola"})

    assert flashes()[-1] == ("error", "No se pudo actualizar el about de 'repo-uno'")


def test_pull_repo_exito(cliente, tmp_path, monkeypatch, flashes):
    (tmp_path / "publico" / "repo-uno").mkdir(parents=True)
    monkeypatch.setattr("app.CARPETA_REPOS", tmp_path)

    with patch("git_ops.subprocess.run") as run_mock:
        run_mock.return_value.returncode = 0
        respuesta = cliente.post("/pull_repo/publico/repo-uno")

    assert respuesta.status_code == 302
    assert flashes()[-1][0] == "success"
    comando = run_mock.call_args[0][0]
    assert comando[:2] == ["git", "-C"]


def test_pull_repo_error(cliente, tmp_path, monkeypatch, flashes):
    (tmp_path / "publico" / "repo-uno").mkdir(parents=True)
    monkeypatch.setattr("app.CARPETA_REPOS", tmp_path)

    with patch("git_ops.subprocess.run") as run_mock:
        run_mock.return_value.returncode = 1
        cliente.post("/pull_repo/publico/repo-uno")

    assert flashes()[-1][0] == "error"


def test_pull_repo_sin_copia_local(cliente, tmp_path, monkeypatch, flashes):
    monkeypatch.setattr("app.CARPETA_REPOS", tmp_path)
    cliente.post("/pull_repo/publico/repo-uno")
    categoria, mensaje = flashes()[-1]
    assert categoria == "error"
    assert "no existe" in mensaje


def test_fetch_repo_exito(cliente, tmp_path, monkeypatch, flashes):
    (tmp_path / "publico" / "repo-uno").mkdir(parents=True)
    monkeypatch.setattr("app.CARPETA_REPOS", tmp_path)

    with patch("git_ops.subprocess.run") as run_mock:
        run_mock.return_value.returncode = 0
        respuesta = cliente.post("/fetch_repo/publico/repo-uno")

    assert respuesta.status_code == 302
    assert flashes()[-1][0] == "success"


def test_elimina_repos_seleccion(cliente, respuesta_fake, flashes):
    with patch("github_api.requests.delete", return_value=respuesta_fake(status_code=204)) as delete_mock:
        respuesta = cliente.post(
            "/elimina_repos",
            data={"seleccionados": ["publico/repo-uno", "privado/repo-dos"]},
        )

    assert respuesta.status_code == 302
    assert delete_mock.call_count == 2
    assert flashes()[-1] == ("success", "2 repositorio(s) eliminados correctamente")


def test_elimina_repos_ignora_valores_invalidos(cliente, respuesta_fake, flashes):
    with patch("github_api.requests.delete", return_value=respuesta_fake(status_code=204)) as delete_mock:
        respuesta = cliente.post(
            "/elimina_repos",
            data={"seleccionados": ["../escape", "publico/", "nada", "nit/.."]},
        )

    assert respuesta.status_code == 302
    delete_mock.assert_not_called()
    assert flashes()[-1] == ("error", "Debes seleccionar al menos un repositorio")


def test_elimina_repos_sin_seleccion(cliente, flashes):
    respuesta = cliente.post("/elimina_repos", data={})
    assert respuesta.status_code == 302
    assert flashes()[-1] == ("error", "Debes seleccionar al menos un repositorio")


def test_clona_repos_seleccion(cliente, flashes, monkeypatch):
    clonados = []

    def clonar_falso(nombre, visibilidad):
        clonados.append((visibilidad, nombre))
        return f"Repositorio '{nombre}' clonado correctamente."

    monkeypatch.setattr(git_ops, "clonar_repo", clonar_falso)
    respuesta = cliente.post(
        "/clona_repos_seleccion",
        data={"seleccionados": ["publico/repo-uno", "privado/repo-dos"]},
    )

    assert respuesta.status_code == 302
    assert sorted(clonados) == [("privado", "repo-dos"), ("publico", "repo-uno")]
    assert flashes()[-1] == ("success", "2 repositorio(s) clonados correctamente")


def test_clona_repos_seleccion_parcial(cliente, flashes, monkeypatch):
    def clonar_falso(nombre, visibilidad):
        return "Error al clonar" if nombre == "repo-dos" else "clonado correctamente."

    monkeypatch.setattr(git_ops, "clonar_repo", clonar_falso)
    cliente.post(
        "/clona_repos_seleccion",
        data={"seleccionados": ["publico/repo-uno", "publico/repo-dos"]},
    )
    assert flashes()[-1] == ("success", "1 repositorio(s) clonados y 1 con errores")


def test_clona_repos_seleccion_sin_seleccion(cliente, flashes):
    cliente.post("/clona_repos_seleccion", data={})
    assert flashes()[-1] == ("error", "Debes seleccionar al menos un repositorio")