const botonesPullRepo = document.querySelectorAll(".boton-pull-repo");
const modalPullRepo = document.getElementById("modal-pull-repo");
const formularioPullRepo = document.getElementById("form-pull-repo");

botonesPullRepo.forEach(boton => {
    boton.addEventListener("click", () => {
        const nombre = boton.dataset.nombre;
        const visibilidad = boton.dataset.visibilidad;

        formularioPullRepo.action = `/pull_repo/${visibilidad}/${nombre}`;
        modalPullRepo.style.display = "flex";
    });
});

const cerrarModalPullRepo = document.getElementById("cerrar-modal-pull-repo");
const botonCerrarModalPullRepo = document.getElementById("boton-cerrar-modal-pull-repo");

cerrarModalPullRepo.addEventListener("click", () => {
    modalPullRepo.style.display = "none";
});

botonCerrarModalPullRepo.addEventListener("click", () => {
    modalPullRepo.style.display = "none";
});

const botonesFetchRepo = document.querySelectorAll(".boton-fetch-repo");
const modalFetchRepo = document.getElementById("modal-fetch-repo");
const formularioFetchRepo = document.getElementById("form-fetch-repo");

botonesFetchRepo.forEach(boton => {
    boton.addEventListener("click", () => {
        const nombre = boton.dataset.nombre;
        const visibilidad = boton.dataset.visibilidad;

        formularioFetchRepo.action = `/fetch_repo/${visibilidad}/${nombre}`;
        modalFetchRepo.style.display = "flex";
    });
});

const cerrarModalFetchRepo = document.getElementById("cerrar-modal-fetch-repo");
const botonCerrarModalFetchRepo = document.getElementById("boton-cerrar-modal-fetch-repo");

cerrarModalFetchRepo.addEventListener("click", () => {
    modalFetchRepo.style.display = "none";
});

botonCerrarModalFetchRepo.addEventListener("click", () => {
    modalFetchRepo.style.display = "none";
});