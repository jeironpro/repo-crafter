const modalCreaRepo = document.getElementById('modal-crea-repo');
const abrirModalCreaRepo = document.getElementById('abrir-modal-crea-repo');
const cerrarModalCreaRepo = document.getElementById('cerrar-modal-crea-repo');

abrirModalCreaRepo.addEventListener("click", () => {
    modalCreaRepo.style.display = 'flex';
});

cerrarModalCreaRepo.addEventListener('click', () => {
    modalCreaRepo.style.display = 'none';
});

modalCreaRepo.addEventListener('click', (e) => {
    if (e.target === modalCreaRepo) {
        modalCreaRepo.style.display = 'none';
    }
});


const modalClonaRepos = document.getElementById('modal-clona-repos');
const abrirModalClonaRepos = document.getElementById('abrir-modal-clona-repos');
const cerrarModalClonaRepos = document.getElementById('cerrar-modal-clona-repos');
const botonCerrarModalClonaRepos = document.getElementById('boton-cerrar-modal-clona-repos');

abrirModalClonaRepos.addEventListener("click", () => {
    modalClonaRepos.style.display = 'flex';
});

botonCerrarModalClonaRepos.addEventListener("click", () => {
    modalClonaRepos.style.display = 'none';
});

cerrarModalClonaRepos.addEventListener('click', () => {
    modalClonaRepos.style.display = 'none';
});

modalClonaRepos.addEventListener('click', (e) => {
    if (e.target === modalClonaRepos) {
        modalClonaRepos.style.display = 'none';
    }
});

const botonesActualizaRepo = document.querySelectorAll(".boton-actualizar");
const modalActualizaRepo = document.getElementById('modal-actualiza-repo');
const formularioCommit = document.getElementById('form-actualiza-repo');

botonesActualizaRepo.forEach(boton => {
    boton.addEventListener("click", async () => {
        const nombre = boton.dataset.nombre;
        const visibilidad = boton.dataset.visibilidad;

        try {
            const respuesta = await fetch(`/estado_repo/${visibilidad}/${nombre}`);

            if (!respuesta.ok) {
                const texto = await respuesta.text();
                throw new Error(`Error: ${texto} - Estado: ${respuesta.status}`);
            }
            const datos = await respuesta.json();

            const lista = document.getElementById("lista-archivos");
            lista.textContent = "";

            if (datos.archivos.length === 0) {
                const elemento = document.createElement("li");
                elemento.classList.add("elemento");
                elemento.textContent = "No hay cambios pendientes";
                lista.appendChild(elemento);
            } else {
                datos.archivos.forEach(({ archivo, estado }) => {
                    const elemento = document.createElement("li");
                    elemento.classList.add("elemento");

                    const inputSelecciona = document.createElement("input");
                    inputSelecciona.type = "checkbox";
                    inputSelecciona.value = archivo;
                    inputSelecciona.checked = true;
                    inputSelecciona.name = "archivos";
                    elemento.appendChild(inputSelecciona);

                    const estadoEl = document.createElement("strong");
                    estadoEl.textContent = estado;
                    elemento.appendChild(estadoEl);

                    const archivoEl = document.createElement("span");
                    archivoEl.textContent = archivo;
                    elemento.appendChild(archivoEl);

                    lista.appendChild(elemento);
                });
            }

            formularioCommit.action = `/commit_repo/${visibilidad}/${nombre}`;
            modalActualizaRepo.style.display = 'flex';
        } catch (error) {
            console.error("Error obteniendo estado del repo:", error);
        }
    });
});


const cerrarModalActualizaRepo = document.getElementById('cerrar-modal-actualiza-repo');
cerrarModalActualizaRepo.addEventListener('click', () => {
    modalActualizaRepo.style.display = 'none';
});

const botonesEliminaRepo = document.querySelectorAll(".boton-eliminar");
const modalEliminaRepo = document.getElementById('modal-elimina-repo');
const formularioElimina = document.getElementById('form-elimina-repo');

botonesEliminaRepo.forEach(boton => {
    boton.addEventListener("click", async () => {
        const nombre = boton.dataset.nombre;

        formularioElimina.action = `/elimina_repo/${nombre}`;
        modalEliminaRepo.style.display = "flex";
    });
});

const cerrarModalEliminaRepo = document.getElementById('cerrar-modal-elimina-repo');
cerrarModalEliminaRepo.addEventListener('click', () => {
    modalEliminaRepo.style.display = 'none';
});

const botonCerrarModalEliminaRepo = document.getElementById('boton-cerrar-modal-elimina-repo');
botonCerrarModalEliminaRepo.addEventListener("click", () => {
    modalEliminaRepo.style.display = 'none';
});

const botonesClonaRepo = document.querySelectorAll(".boton-clonar");
const modalClonaRepo = document.getElementById('modal-clona-repo');
const formularioClona = document.getElementById('form-clona-repo');

botonesClonaRepo.forEach(boton => {
    boton.addEventListener("click", async () => {
        const nombre = boton.dataset.nombre;
        const visibilidad = boton.dataset.visibilidad;

        formularioClona.action = `/clona_repo/${nombre}/${visibilidad}`;
        modalClonaRepo.style.display = "flex";
    });
});

const cerrarModalClonaRepo = document.getElementById('cerrar-modal-clona-repo');
cerrarModalClonaRepo.addEventListener('click', () => {
    modalClonaRepo.style.display = 'none';
});

const botonCerrarModalClonaRepo = document.getElementById('boton-cerrar-modal-clona-repo');
botonCerrarModalClonaRepo.addEventListener("click", () => {
    modalClonaRepo.style.display = 'none';
});