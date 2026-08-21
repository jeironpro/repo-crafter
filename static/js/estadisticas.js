document.documentElement.classList.add('js');

const reduceMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function animarContador(elemento) {
    const destino = parseInt(elemento.textContent, 10);
    if (Number.isNaN(destino) || reduceMovimiento || destino === 0) return;

    const duracion = 900;
    const inicio = performance.now();

    function paso(ahora) {
        const progreso = Math.min((ahora - inicio) / duracion, 1);
        const eased = 1 - Math.pow(1 - progreso, 3);
        elemento.textContent = Math.round(eased * destino);
        if (progreso < 1) requestAnimationFrame(paso);
    }

    requestAnimationFrame(paso);
}

const contadores = document.querySelectorAll('.valor');
const tarjetas = document.querySelectorAll('.tarjeta-repo, .contenedor-estadisticas');

if ('IntersectionObserver' in window && !reduceMovimiento) {
    const observador = new IntersectionObserver(entradas => {
        entradas.forEach(entrada => {
            if (!entrada.isIntersecting) return;
            entrada.target.classList.add('is-in');
            if (entrada.target.classList.contains('contenedor-estadisticas')) {
                entrada.target.querySelectorAll('.valor').forEach(animarContador);
            }
            observador.unobserve(entrada.target);
        });
    }, { threshold: 0.15 });

    tarjetas.forEach(tarjeta => observador.observe(tarjeta));
} else {
    tarjetas.forEach(tarjeta => tarjeta.classList.add('is-in'));
}
