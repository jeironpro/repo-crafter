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
        const visibilidad = tarjeta.dataset.visibilidad || "";
        const pagina = (tarjeta.dataset.pagina || "").replace(/-/g, " ");
        const topics = tarjeta.dataset.topics ? tarjeta.dataset.topics.split(",") : [];

        const coincideTexto = nombre.includes(texto) || visibilidad.includes(texto) || pagina.includes(texto);
        const coincideTema = !tema || topics.includes(tema);

        tarjeta.classList.toggle("oculta", !(coincideTexto && coincideTema));
    });

    if (typeof window.actualizarPaginacion === "function") {
        window.actualizarPaginacion();
    }
}

function sincronizarFiltros() {
    const estado = window.estadoUrl ? window.estadoUrl.leer() : {};
    buscador.value = estado.q || "";
    filtroTema.value = estado.tema || "";
    filtrarRepos();
}

buscador.addEventListener("input", () => {
    filtrarRepos();
    window.estadoUrl?.escribir({ q: buscador.value || null, page: null }, true);
});

filtroTema.addEventListener("change", () => {
    filtrarRepos();
    window.estadoUrl?.escribir({ tema: filtroTema.value || null, page: null });
});

window.addEventListener("popstate", sincronizarFiltros);

sincronizarFiltros();
