const botonesTopicsRepo = document.querySelectorAll(".boton-topics-repo");
const modalTopicsRepo = document.getElementById("modal-topics-repo");
const tituloModalTopics = document.getElementById("titulo-modal-topics");
const cerrarModalTopicsRepo = document.getElementById("cerrar-modal-topics-repo");
const formTopicsRepo = document.getElementById("form-topics-repo");
const chipsTopics = document.getElementById("chips-topics");
const entradaTopic = document.getElementById("entrada-topic");
const topicsFinales = document.getElementById("topics-finales");

let topicsActuales = [];

function sincronizar() {
    topicsFinales.value = topicsActuales.join(",");
}

function pintarChips() {
    chipsTopics.innerHTML = "";

    topicsActuales.forEach((topic, indice) => {
        const chip = document.createElement("span");
        chip.className = "chip-topic";
        chip.append(document.createTextNode(topic));

        const equis = document.createElement("button");
        equis.type = "button";
        equis.className = "chip-topic__x";
        equis.setAttribute("aria-label", `Quitar ${topic}`);
        equis.textContent = "×";
        equis.addEventListener("click", () => {
            topicsActuales.splice(indice, 1);
            pintarChips();
        });

        chip.appendChild(equis);
        chipsTopics.appendChild(chip);
    });

    sincronizar();
}

function agregarTopic(valor) {
    const topic = valor.trim().toLowerCase().replace(/\s+/g, "-");

    if (!topic || topicsActuales.includes(topic)) return;

    topicsActuales.push(topic);
    pintarChips();
}

botonesTopicsRepo.forEach(boton => {
    boton.addEventListener("click", () => {
        const nombre = boton.dataset.nombre;

        tituloModalTopics.textContent = `Topics · ${nombre}`;
        formTopicsRepo.action = `/topics/${nombre}`;
        topicsActuales = boton.dataset.topics ? boton.dataset.topics.split(",").filter(Boolean) : [];
        entradaTopic.value = "";
        pintarChips();

        modalTopicsRepo.style.display = "flex";
        entradaTopic.focus();
    });
});

entradaTopic.addEventListener("keydown", evento => {
    if (evento.key === "Enter" || evento.key === ",") {
        evento.preventDefault();
        agregarTopic(entradaTopic.value);
        entradaTopic.value = "";
    }
});

formTopicsRepo.addEventListener("submit", sincronizar);

cerrarModalTopicsRepo.addEventListener("click", () => {
    modalTopicsRepo.style.display = "none";
});

modalTopicsRepo.addEventListener("click", evento => {
    if (evento.target === modalTopicsRepo) {
        modalTopicsRepo.style.display = "none";
    }
});
