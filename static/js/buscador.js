function eliminarAcentos(texto) {
    return texto.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

const buscador = document.getElementById("buscador");
const filtroTema = document.getElementById("filtro-tema");
const tarjetasRepo = document.querySelectorAll(".tarjeta-repo");

function filtrarRepos() {
    const texto = eliminarAcentos(buscador.value.toLowerCase());
    const tema = filtroTema.value;

    tarjetasRepo.forEach(tarjeta => {
        const nombre = eliminarAcentos(tarjeta.querySelector(".tarjeta-nombre").textContent.toLowerCase());
        const filas = tarjeta.querySelectorAll(".tarjeta-fila");
        const topics = tarjeta.dataset.topics ? tarjeta.dataset.topics.split(",") : [];

        let visibilidad = "";
        let pagina = "";

        filas.forEach(fila => {
            const etiqueta = eliminarAcentos(fila.querySelector(".tarjeta-etiqueta").textContent.toLowerCase());
            const valor = eliminarAcentos(fila.querySelector(".tarjeta-valor").textContent.toLowerCase());

            if (etiqueta.includes("visibilidad")) {
                visibilidad = valor;
            } else if (etiqueta.includes("página")) {
                pagina = valor;
            }
        });

        const coincideTexto = nombre.includes(texto) || visibilidad.includes(texto) || pagina.includes(texto);
        const coincideTema = !tema || topics.includes(tema);

        if (coincideTexto && coincideTema) {
            tarjeta.style.display = '';
        } else {
            tarjeta.style.display = 'none';
        }
    });
}

buscador.addEventListener("input", filtrarRepos);
filtroTema.addEventListener("change", filtrarRepos);
