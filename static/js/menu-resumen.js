const botonResumen = document.getElementById("boton-resumen");
const listaResumen = document.getElementById("menu-resumen-lista");

if (botonResumen && listaResumen) {
    function cerrarMenuResumen() {
        listaResumen.hidden = true;
        botonResumen.setAttribute("aria-expanded", "false");
    }

    botonResumen.addEventListener("click", evento => {
        evento.stopPropagation();
        const abrir = listaResumen.hidden;
        listaResumen.hidden = !abrir;
        botonResumen.setAttribute("aria-expanded", String(abrir));
    });

    listaResumen.addEventListener("click", () => cerrarMenuResumen());

    document.addEventListener("click", evento => {
        if (!listaResumen.hidden && !evento.target.closest(".menu-resumen")) {
            cerrarMenuResumen();
        }
    });

    document.addEventListener("keydown", evento => {
        if (evento.key === "Escape" && !listaResumen.hidden) {
            cerrarMenuResumen();
            botonResumen.focus();
        }
    });
}
