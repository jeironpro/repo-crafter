const botonesArchivosRepo = document.querySelectorAll(".boton-archivos-repo");
const modalArchivosRepo = document.getElementById("modal-archivos-repo");
const tituloModalArchivos = document.getElementById("titulo-modal-archivos");
const cerrarModalArchivosRepo = document.getElementById("cerrar-modal-archivos-repo");
const breadcrumb = document.getElementById("breadcrumb-archivos");
const listaExplorador = document.getElementById("lista-explorador");
const vacioExplorador = document.getElementById("vacio-explorador");

const modalVerArchivo = document.getElementById("modal-ver-archivo");
const tituloVerArchivo = document.getElementById("titulo-modal-ver-archivo");
const cerrarModalVerArchivo = document.getElementById("cerrar-modal-ver-archivo");
const contenidoArchivo = document.getElementById("contenido-archivo");
const codigoArchivo = contenidoArchivo.querySelector("code");
const errorVisor = document.getElementById("error-visor");

let contexto = { nombre: "", ruta: "" };

function rutaExplorador() {
    const parametros = contexto.ruta ? `?ruta=${encodeURIComponent(contexto.ruta)}` : "";
    return `/archivos/${contexto.nombre}${parametros}`;
}

function pintarBreadcrumb() {
    breadcrumb.innerHTML = "";

    const agregar = (etiqueta, ruta) => {
        const boton = document.createElement("button");
        boton.type = "button";
        boton.textContent = etiqueta;
        if (ruta === contexto.ruta) boton.setAttribute("aria-current", "location");
        boton.addEventListener("click", () => abrirEn(ruta));
        breadcrumb.appendChild(boton);
    };

    agregar("raiz", "");
    let acumulado = "";
    contexto.ruta.split("/").filter(Boolean).forEach(parte => {
        acumulado = acumulado ? `${acumulado}/${parte}` : parte;
        agregar(parte, acumulado);
    });
}

function crearFila(icono, etiqueta, accion) {
    const elemento = document.createElement("li");

    const boton = document.createElement("button");
    boton.type = "button";
    const simbolo = document.createElement("span");
    simbolo.className = "material-symbols-outlined";
    simbolo.setAttribute("aria-hidden", "true");
    simbolo.textContent = icono;
    boton.append(simbolo, document.createTextNode(etiqueta));
    boton.addEventListener("click", accion);

    elemento.appendChild(boton);
    return elemento;
}

function pintarListado(datos) {
    listaExplorador.innerHTML = "";

    datos.carpetas.forEach(carpeta => {
        listaExplorador.appendChild(crearFila("folder", carpeta.nombre, () => {
            abrirEn(contexto.ruta ? `${contexto.ruta}/${carpeta.nombre}` : carpeta.nombre);
        }));
    });

    datos.archivos.forEach(archivo => {
        listaExplorador.appendChild(crearFila("description", archivo.nombre, () => verArchivo(archivo.nombre)));
    });

    vacioExplorador.hidden = (datos.carpetas.length + datos.archivos.length) > 0;
}

async function abrirEn(ruta) {
    contexto.ruta = ruta;
    listaExplorador.innerHTML = "";
    vacioExplorador.hidden = true;

    try {
        const respuesta = await fetch(rutaExplorador());
        if (!respuesta.ok) throw new Error();
        pintarBreadcrumb();
        pintarListado(await respuesta.json());
    } catch {
        vacioExplorador.textContent = "No se pudo leer la carpeta";
        vacioExplorador.hidden = false;
    }
}

async function verArchivo(nombreArchivo) {
    const rutaCompleta = contexto.ruta ? `${contexto.ruta}/${nombreArchivo}` : nombreArchivo;

    tituloVerArchivo.textContent = nombreArchivo;
    errorVisor.hidden = true;
    contenidoArchivo.hidden = true;
    modalVerArchivo.style.display = "flex";

    try {
        const respuesta = await fetch(
            `/archivo/${contexto.nombre}?ruta=${encodeURIComponent(rutaCompleta)}`
        );
        const datos = await respuesta.json();

        if (!respuesta.ok) throw new Error(datos.error || "No se pudo leer el archivo");

        codigoArchivo.textContent = datos.contenido;
        contenidoArchivo.hidden = false;
    } catch (error) {
        errorVisor.textContent = error.message;
        errorVisor.hidden = false;
    }
}

botonesArchivosRepo.forEach(boton => {
    boton.addEventListener("click", () => {
        contexto = {
            nombre: boton.dataset.nombre,
            ruta: ""
        };

        tituloModalArchivos.textContent = `Archivos · ${contexto.nombre}`;
        vacioExplorador.textContent = "Carpeta vacia";
        modalArchivosRepo.style.display = "flex";
        abrirEn("");
    });
});

cerrarModalArchivosRepo.addEventListener("click", () => {
    modalArchivosRepo.style.display = "none";
});

modalArchivosRepo.addEventListener("click", evento => {
    if (evento.target === modalArchivosRepo) {
        modalArchivosRepo.style.display = "none";
    }
});

cerrarModalVerArchivo.addEventListener("click", () => {
    modalVerArchivo.style.display = "none";
});

modalVerArchivo.addEventListener("click", evento => {
    if (evento.target === modalVerArchivo) {
        modalVerArchivo.style.display = "none";
    }
});

document.addEventListener("keydown", evento => {
    if (evento.key !== "Escape") return;

    const abiertos = [...document.querySelectorAll(".contenedor-modal")]
        .filter(modal => modal.style.display === "flex")
        .sort((a, b) =>
            (parseInt(getComputedStyle(b).zIndex, 10) || 0) -
            (parseInt(getComputedStyle(a).zIndex, 10) || 0)
        );

    if (abiertos[0]) abiertos[0].style.display = "none";
});
