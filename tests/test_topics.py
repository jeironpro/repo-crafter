from unittest.mock import patch

from tests.conftest import RespuestaFake


def test_guarda_topics_envia_lista_normalizada(cliente, respuesta_fake, flashes):
    with patch("github_api.actualizar_topics", return_value=respuesta_fake(status_code=200)) as actualizar:
        cliente.post("/topics/repo-uno", data={"topics": "  Flask , Mi-Topic,,API"})

    assert actualizar.call_args[0] == ("repo-uno", ["flask", "mi-topic", "api"])
    assert ("success", "Topics de 'repo-uno' actualizados correctamente") in flashes()


def test_guarda_topics_rechaza_mas_de_veinte(cliente, flashes):
    topics = ",".join(f"topic-{i}" for i in range(21))

    cliente.post("/topics/repo-uno", data={"topics": topics})

    assert ("error", "Un repositorio puede tener como máximo 20 topics") in flashes()


def test_guarda_topics_rechaza_formatos_invalidos(cliente, flashes):
    cliente.post("/topics/repo-uno", data={"topics": "valido,Mal Topic,con_underscore"})

    mensajes = [texto for _, texto in flashes()]
    assert any("Topics inválidos" in texto for texto in mensajes)


def test_guarda_topics_reporta_error_de_api(cliente, respuesta_fake, flashes):
    with patch("github_api.actualizar_topics", return_value=respuesta_fake(status_code=422)):
        cliente.post("/topics/repo-uno", data={"topics": "flask"})

    assert ("error", "No se pudieron actualizar los topics de 'repo-uno'") in flashes()


def test_guarda_topics_valida_nombre(cliente):
    assert cliente.post("/topics/nombre%20invalido", data={"topics": "a"}).status_code == 404


def test_limpiar_cache_se_llama_al_actualizar_topics(cliente, respuesta_fake):
    with patch("github_api.actualizar_topics", return_value=respuesta_fake(status_code=200)), \
         patch("github_api.limpiar_cache") as limpiar:
        cliente.post("/topics/repo-uno", data={"topics": "flask"})

    limpiar.assert_called_once()
