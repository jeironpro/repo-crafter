const modalContenedor = document.querySelector('.contenedor-modal');
const botonCerrar = document.querySelector('.cabecera-modal span');

function abrirModal() {
    modalContenedor.style.display = 'flex';
}

botonCerrar.addEventListener('click', () => {
    modalContenedor.style.display = 'none';
});

modalContenedor.addEventListener('click', (e) => {
    if (e.target === modalContenedor) {
        modalContenedor.style.display = 'none';
    }
});
