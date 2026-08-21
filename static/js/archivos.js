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
let restaurando = false;

const PATRON_NOMBRE = /^[A-Za-z0-9_.-]+$/;

function actualizarBloqueoScroll() {
    const algunoAbierto = [...document.querySelectorAll(".contenedor-modal")]
        .some(modal => modal.style.display === "flex");
    document.body.style.overflow = algunoAbierto ? "hidden" : "";
}

function fijarDisplay(modal, valor) {
    modal.style.display = valor;
    actualizarBloqueoScroll();
}

function rutaExplorador() {
    const parametros = contexto.ruta ? `?ruta=${encodeURIComponent(contexto.ruta)}` : "";
    return `/archivos/${contexto.nombre}${parametros}`;
}

function carpetaDeRuta(ruta) {
    const partes = ruta.split("/").filter(Boolean);
    partes.pop();
    return partes.join("/");
}

function pintarBreadcrumb() {
    breadcrumb.innerHTML = "";

    const agregar = (etiqueta, ruta) => {
        const boton = document.createElement("button");
        boton.type = "button";
        boton.textContent = etiqueta;
        if (ruta === contexto.ruta) boton.setAttribute("aria-current", "location");
        boton.addEventListener("click", () => navegarA(ruta));
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
        const destino = contexto.ruta ? `${contexto.ruta}/${carpeta.nombre}` : carpeta.nombre;
        listaExplorador.appendChild(crearFila("folder", carpeta.nombre, () => navegarA(destino)));
    });

    datos.archivos.forEach(archivo => {
        listaExplorador.appendChild(crearFila("description", archivo.nombre, () => verArchivo(archivo.nombre)));
    });

    vacioExplorador.hidden = (datos.carpetas.length + datos.archivos.length) > 0;
}

function navegarA(ruta) {
    window.estadoUrl?.escribir({ repo: contexto.nombre, ruta: ruta || null });
    abrirEn(ruta);
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
    await verArchivoRuta(rutaCompleta);
}

async function verArchivoRuta(rutaCompleta) {
    let respuesta;
    try {
        respuesta = await fetch(
            `/archivo/${contexto.nombre}?ruta=${encodeURIComponent(rutaCompleta)}`
        );
    } catch {
        return false;
    }

    if (respuesta.status === 404) return false;

    tituloVerArchivo.textContent = rutaCompleta.split("/").pop();
    errorVisor.hidden = true;
    contenidoArchivo.hidden = true;
    fijarDisplay(modalVerArchivo, "flex");

    try {
        const datos = await respuesta.json();

        if (!respuesta.ok) throw new Error(datos.error || "No se pudo leer el archivo");

        codigoArchivo.textContent = datos.contenido;
        contenidoArchivo.hidden = false;
    } catch (error) {
        errorVisor.textContent = error.message;
        errorVisor.hidden = false;
    }

    return true;
}

function prepararExplorador(nombre) {
    contexto = { nombre: nombre, ruta: "" };
    tituloModalArchivos.textContent = `Archivos · ${contexto.nombre}`;
    vacioExplorador.textContent = "Carpeta vacia";
    fijarDisplay(modalArchivosRepo, "flex");
}

botonesArchivosRepo.forEach(boton => {
    boton.addEventListener("click", () => {
        prepararExplorador(boton.dataset.nombre);
        window.estadoUrl?.escribir({ repo: contexto.nombre, ruta: null });
        abrirEn("");
    });
});

function cerrarVisor() {
    fijarDisplay(modalVerArchivo, "none");
    if (!restaurando) {
        window.estadoUrl?.escribir({ repo: contexto.nombre, ruta: contexto.ruta || null }, true);
    }
}

function cerrarExplorador() {
    fijarDisplay(modalArchivosRepo, "none");
    if (!restaurando) {
        window.estadoUrl?.escribir({ repo: null, ruta: null });
    }
}

cerrarModalArchivosRepo.addEventListener("click", cerrarExplorador);

modalArchivosRepo.addEventListener("click", evento => {
    if (evento.target === modalArchivosRepo) cerrarExplorador();
});

cerrarModalVerArchivo.addEventListener("click", cerrarVisor);

modalVerArchivo.addEventListener("click", evento => {
    if (evento.target === modalVerArchivo) cerrarVisor();
});

document.addEventListener("keydown", evento => {
    if (evento.key !== "Escape") return;

    const abiertos = [...document.querySelectorAll(".contenedor-modal")]
        .filter(modal => modal.style.display === "flex")
        .sort((a, b) =>
            (parseInt(getComputedStyle(b).zIndex, 10) || 0) -
            (parseInt(getComputedStyle(a).zIndex, 10) || 0)
        );

    if (!abiertos[0]) return;

    if (abiertos[0] === modalVerArchivo) cerrarVisor();
    else if (abiertos[0] === modalArchivosRepo) cerrarExplorador();
    else fijarDisplay(abiertos[0], "none");
});

async function restaurarDesdeUrl() {
    const estado = window.estadoUrl ? window.estadoUrl.leer() : {};

    if (!estado.repo || !PATRON_NOMBRE.test(estado.repo)) {
        if (modalVerArchivo.style.display === "flex") fijarDisplay(modalVerArchivo, "none");
        if (modalArchivosRepo.style.display === "flex") cerrarExplorador();
        return;
    }

    restaurando = true;
    prepararExplorador(estado.repo);

    if (estado.ruta) {
        const esArchivo = await verArchivoRuta(estado.ruta);
        await abrirEn(esArchivo ? carpetaDeRuta(estado.ruta) : estado.ruta);
    } else {
        await abrirEn("");
    }

    restaurando = false;
}

window.addEventListener("popstate", restaurarDesdeUrl);
restaurarDesdeUrl();
