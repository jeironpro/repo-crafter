const botonAbrirSeleccion = document.getElementById("abrir-seleccion");
const barraSeleccion = document.getElementById("barra-seleccion");
const conteoSeleccion = document.getElementById("seleccion-conteo");
const seleccionarTodos = document.getElementById("seleccionar-todos");
const botonCancelarSeleccion = document.getElementById("boton-cancelar-seleccion");
const botonClonaSeleccion = document.getElementById("boton-clona-seleccion");
const botonEliminaSeleccion = document.getElementById("boton-elimina-seleccion");

const modalClonaSeleccion = document.getElementById("modal-clona-seleccion");
const modalEliminaSeleccion = document.getElementById("modal-elimina-seleccion");
const listaClonaSeleccion = document.getElementById("lista-clona-seleccion");
const listaEliminaSeleccion = document.getElementById("lista-elimina-seleccion");
const formClonaSeleccion = document.getElementById("form-clona-seleccion");
const formEliminaSeleccion = document.getElementById("form-elimina-seleccion");

const cerrarClonaSeleccion = document.getElementById("cerrar-modal-clona-seleccion");
const cerrarEliminaSeleccion = document.getElementById("cerrar-modal-elimina-seleccion");
const botonCerrarClonaSeleccion = document.getElementById("boton-cerrar-modal-clona-seleccion");
const botonCerrarEliminaSeleccion = document.getElementById("boton-cerrar-modal-elimina-seleccion");

const contenedorTarjetas = document.querySelector(".contenedor-repos");

if (botonAbrirSeleccion && contenedorTarjetas) {
    const tarjetas = Array.from(contenedorTarjetas.querySelectorAll(".tarjeta-repo"));
    const seleccion = new Map();

    let modoSeleccion = false;

    function nombreTarjeta(tarjeta) {
        return tarjeta.querySelector(".enlace-repo").textContent.trim();
    }

    function tarjetaVisible(tarjeta) {
        return !tarjeta.classList.contains("oculta") && tarjeta.style.display !== "none";
    }

    function seleccionarTarjeta(tarjeta, estado) {
        const nombre = nombreTarjeta(tarjeta);
        const checkbox = tarjeta._seleccionCheckbox;

        if (estado) {
            seleccion.set(nombre, tarjeta.dataset.visibilidad);
            tarjeta.classList.add("is-seleccionado");
            checkbox.checked = true;
        } else {
            seleccion.delete(nombre);
            tarjeta.classList.remove("is-seleccionado");
            checkbox.checked = false;
        }
    }

    function actualizarSeleccion() {
        const total = seleccion.size;
        conteoSeleccion.textContent = `${total} seleccionado${total === 1 ? "" : "s"}`;

        botonClonaSeleccion.disabled = total === 0;
        botonEliminaSeleccion.disabled = total === 0;

        const visibles = tarjetas.filter(tarjetaVisible);
        const seleccionadosVisibles = visibles.filter(tarjeta => tarjeta.classList.contains("is-seleccionado")).length;

        seleccionarTodos.checked = visibles.length > 0 && seleccionadosVisibles === visibles.length;
        seleccionarTodos.indeterminate = seleccionadosVisibles > 0 && seleccionadosVisibles < visibles.length;
    }

    function activarSeleccion() {
        modoSeleccion = true;
        botonAbrirSeleccion.setAttribute("aria-pressed", "true");
        contenedorTarjetas.classList.add("modo-seleccion");
        barraSeleccion.hidden = false;
        actualizarSeleccion();
    }

    function desactivarSeleccion() {
        modoSeleccion = false;
        botonAbrirSeleccion.setAttribute("aria-pressed", "false");
        contenedorTarjetas.classList.remove("modo-seleccion");
        barraSeleccion.hidden = true;
        seleccion.clear();

        tarjetas.forEach(tarjeta => {
            tarjeta.classList.remove("is-seleccionado");
            tarjeta._seleccionCheckbox.checked = false;
        });

        actualizarSeleccion();
    }

    tarjetas.forEach(tarjeta => {
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.className = "seleccion-checkbox";
        checkbox.setAttribute("aria-label", `Seleccionar ${nombreTarjeta(tarjeta)}`);

        tarjeta._seleccionCheckbox = checkbox;
        tarjeta.querySelector(".tarjeta-nombre").appendChild(checkbox);

        checkbox.addEventListener("change", () => {
            if (checkbox.checked) {
                const nombre = nombreTarjeta(tarjeta);
                seleccion.set(nombre, tarjeta.dataset.visibilidad);
                tarjeta.classList.add("is-seleccionado");
            } else {
                seleccion.delete(nombreTarjeta(tarjeta));
                tarjeta.classList.remove("is-seleccionado");
            }
            actualizarSeleccion();
        });
    });

    botonAbrirSeleccion.addEventListener("click", () => {
        if (modoSeleccion) {
            desactivarSeleccion();
        } else {
            activarSeleccion();
        }
    });

    botonCancelarSeleccion.addEventListener("click", desactivarSeleccion);

    seleccionarTodos.addEventListener("change", () => {
        tarjetas.filter(tarjetaVisible).forEach(tarjeta => seleccionarTarjeta(tarjeta, seleccionarTodos.checked));
        actualizarSeleccion();
    });

    function poblarModalSeleccion(modal, lista, form) {
        form.querySelectorAll("input[name='seleccionados']").forEach(input => input.remove());
        lista.textContent = "";

        seleccion.forEach((visibilidad, nombre) => {
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "seleccionados";
            input.value = `${visibilidad}/${nombre}`;
            form.appendChild(input);

            const elemento = document.createElement("li");
            elemento.textContent = nombre;
            lista.appendChild(elemento);
        });

        modal.style.display = "flex";
    }

    botonClonaSeleccion.addEventListener("click", () => {
        if (seleccion.size === 0) return;
        poblarModalSeleccion(modalClonaSeleccion, listaClonaSeleccion, formClonaSeleccion);
    });

    botonEliminaSeleccion.addEventListener("click", () => {
        if (seleccion.size === 0) return;
        poblarModalSeleccion(modalEliminaSeleccion, listaEliminaSeleccion, formEliminaSeleccion);
    });

    [cerrarClonaSeleccion, botonCerrarClonaSeleccion].forEach(elemento => {
        elemento.addEventListener("click", () => {
            modalClonaSeleccion.style.display = "none";
        });
    });

    [cerrarEliminaSeleccion, botonCerrarEliminaSeleccion].forEach(elemento => {
        elemento.addEventListener("click", () => {
            modalEliminaSeleccion.style.display = "none";
        });
    });

    modalClonaSeleccion.addEventListener("click", evento => {
        if (evento.target === modalClonaSeleccion) {
            modalClonaSeleccion.style.display = "none";
        }
    });

    modalEliminaSeleccion.addEventListener("click", evento => {
        if (evento.target === modalEliminaSeleccion) {
            modalEliminaSeleccion.style.display = "none";
        }
    });
}