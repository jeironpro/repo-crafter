import os

os.environ.setdefault("GITHUB_USER", "usuario-test")
os.environ.setdefault("GITHUB_EMAIL", "correo@test.com")
os.environ.setdefault("GITHUB_TOKEN", "token-test")

import pytest

import github_api
from app import app as app_flask


@pytest.fixture(autouse=True)
def limpiar_cache_api():
    github_api.limpiar_cache()
    yield
    github_api.limpiar_cache()


class RespuestaFake:
    def __init__(self, datos=None, status_code=200, texto=""):
        self.datos = datos if datos is not None else []
        self.status_code = status_code
        self.text = texto

    def json(self):
        return self.datos

    @property
    def ok(self):
        return 200 <= self.status_code < 300


@pytest.fixture()
def respuesta_fake():
    return RespuestaFake


@pytest.fixture()
def repo_falso():
    def _crear(nombre="repo-uno", privado=False, paginas=False, topics=None):
        return {
            "name": nombre,
            "private": privado,
            "has_pages": paginas,
            "topics": topics or [],
            "svn_url": f"https://github.com/usuario-test/{nombre}",
            "ssh_url": f"git@github.com:usuario-test/{nombre}.git",
            "owner": {"login": "usuario-test"},
        }

    return _crear


@pytest.fixture()
def cliente():
    app_flask.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app_flask.test_client() as cliente:
        yield cliente


@pytest.fixture()
def flashes(cliente):
    def _obtener():
        with cliente.session_transaction() as sesion:
            return sesion.get("_flashes", [])

    return _obtener
