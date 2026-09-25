import pytest

from contenido_readmes import CONTENIDO
from reescribir_readmes import (
    TEXTO_LICENCIA,
    contiene_emojis,
    generar_readme,
    reescribir_readme,
)


def test_contiene_emojis_detecta_emojis():
    assert contiene_emojis("Hola 📌")
    assert contiene_emojis("Hola ✨")
    assert not contiene_emojis("Aplicación web del tiempo.")
    assert not contiene_emojis("Años, meses, 100 % y 9x9.")


def test_generar_readme_mantiene_titulo_con_nombre_del_repo():
    contenido = generar_readme("web-clima", CONTENIDO["publico/web-clima"])
    assert contenido.startswith("# web-clima\n")


def test_generar_readme_incluye_secciones_profesionales():
    contenido = generar_readme("web-clima", CONTENIDO["publico/web-clima"])
    assert "## Características" in contenido
    assert "## Tecnologías" in contenido
    assert contenido.count("## ") >= 2


def test_generar_readme_termina_con_la_licencia_exacta():
    contenido = generar_readme("web-clima", CONTENIDO["publico/web-clima"])
    assert contenido.rstrip().endswith(TEXTO_LICENCIA)
    assert "licencia **MIT**.  \nConsulta" in contenido


def test_generar_readme_no_tiene_emojis_ni_plantilla_antigua():
    contenido = generar_readme("web-clima", CONTENIDO["publico/web-clima"])
    assert not contiene_emojis(contenido)
    assert "## 📌 Descripción" not in contenido
    assert "portafolio personal" not in contenido


def test_reescribir_readme_escribe_el_archivo(tmp_path):
    ruta = tmp_path / "README.md"
    reescribir_readme(ruta, "web-clima", CONTENIDO["publico/web-clima"])
    with open(ruta, encoding="utf-8") as archivo:
        assert archivo.read() == generar_readme("web-clima", CONTENIDO["publico/web-clima"])


def test_generar_readme_rechaza_entradas_con_emojis():
    entrada = ("Hola", ("Características", "Texto con emoji 📌"))
    with pytest.raises(ValueError, match="emojis"):
        generar_readme("web-clima", entrada)


def test_contenido_cubre_todos_los_repos():
    assert len(CONTENIDO) == 36
    nombres = {clave.split("/", 1)[1] for clave in CONTENIDO}
    for repo in [
        "alpha-inventory-django", "alpha-inventory-flask", "cursos-infotep-virtual",
        "juego-7-letras", "web-clima", "web-conversor-universal", "web-tests-daw",
    ]:
        assert repo in nombres


def test_todas_las_entradas_generan_readme_valido():
    for ruta, entrada in CONTENIDO.items():
        nombre = ruta.split("/", 1)[1]
        contenido = generar_readme(nombre, entrada)
        assert contenido.startswith(f"# {nombre}\n"), ruta
        assert contenido.count("## ") >= 2, ruta
        assert contenido.rstrip().endswith(TEXTO_LICENCIA), ruta
        assert not contiene_emojis(contenido), ruta
        assert "## 📌 Descripción" not in contenido, ruta
        assert "portafolio personal" not in contenido, ruta
        assert contenido.strip(), ruta
