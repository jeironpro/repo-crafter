document.querySelectorAll('.tarjeta-header').forEach(header => {
    header.addEventListener('click', evento => {
        if (evento.target.closest('button, a, input, form')) return;
        const repo = header.closest('.tarjeta-repo');
        if (window.innerWidth <= 768) {
            repo.classList.toggle('expandido');
        }
    });
});
