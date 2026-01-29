function eliminarAcentos(texto) {
    return texto.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

const buscador = document.getElementById("buscador");
const tarjetasRepo = document.querySelectorAll(".tarjeta-repo");

buscador.addEventListener("input", function() {
    const filtro = eliminarAcentos(this.value.toLowerCase());

    tarjetasRepo.forEach(tarjeta => {
        const nombre = eliminarAcentos(tarjeta.querySelector(".tarjeta-nombre").textContent.toLowerCase());
        const filas = tarjeta.querySelectorAll(".tarjeta-fila");
        
        let visibilidad = "";
        let pagina = "";
        
        // Buscar información de visibilidad y página en las filas
        filas.forEach(fila => {
            const etiqueta = eliminarAcentos(fila.querySelector(".tarjeta-etiqueta").textContent.toLowerCase());
            const valor = eliminarAcentos(fila.querySelector(".tarjeta-valor").textContent.toLowerCase());
            
            if (etiqueta.includes("visibilidad")) {
                visibilidad = valor;
            } else if (etiqueta.includes("página")) {
                pagina = valor;
            }
        });
        
        if (nombre.includes(filtro) || visibilidad.includes(filtro) || pagina.includes(filtro)) {
            tarjeta.style.display = '';
        } else {
            tarjeta.style.display = 'none';
        }
    });
});