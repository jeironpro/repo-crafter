const botonesAboutRepo = document.querySelectorAll(".boton-about-repo");
const modalAboutRepo = document.getElementById("modal-about-repo");
const tituloModalAbout = document.getElementById("titulo-modal-about");
const cerrarModalAboutRepo = document.getElementById("cerrar-modal-about-repo");
const formAboutRepo = document.getElementById("form-about-repo");
const inputDescripcionAbout = document.getElementById("descripcion-about");
const inputWebAbout = document.getElementById("web-about");

botonesAboutRepo.forEach(boton => {
    boton.addEventListener("click", async () => {
        const nombre = boton.dataset.nombre;

        try {
            const respuesta = await fetch(`/about_repo/${encodeURIComponent(nombre)}`);

            if (!respuesta.ok) {
                throw new Error(`Error cargando el about: ${respuesta.status}`);
            }

            const datos = await respuesta.json();

            tituloModalAbout.textContent = `About · ${nombre}`;
            inputDescripcionAbout.value = datos.descripcion || "";
            inputWebAbout.value = datos.web || "";
            formAboutRepo.action = `/about/${nombre}`;
            modalAboutRepo.style.display = "flex";
        } catch (error) {
            console.error("Error obteniendo el about del repo:", error);
        }
    });
});

cerrarModalAboutRepo.addEventListener("click", () => {
    modalAboutRepo.style.display = "none";
});

modalAboutRepo.addEventListener("click", evento => {
    if (evento.target === modalAboutRepo) {
        modalAboutRepo.style.display = "none";
    }
});