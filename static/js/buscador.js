function eliminarAcentos(texto) {
    return texto.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

const buscador = document.getElementById("buscador");
const tabla = document.getElementById("tabla-repos");
const filas = tabla.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
const totalRepos = document.getElementById("total-repos");

buscador.addEventListener("input", function() {
    const filtro = this.value.toLowerCase();
    let contador = 0;

    for (let i = 0; i < filas.length; i++) {
        const nombre = eliminarAcentos(filas[i].getElementsByTagName("td")[0].textContent.toLowerCase());
        const visibilidad = eliminarAcentos(filas[i].getElementsByTagName('td')[1].textContent.toLowerCase());
        
        if (nombre.includes(filtro) || visibilidad.includes(filtro)) {
            filas[i].style.display = '';
            contador++;
        } else {
            filas[i].style.display = 'none';
        }
    }
    totalRepos.textContent = contador;
});