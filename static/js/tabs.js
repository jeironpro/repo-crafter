document.querySelectorAll('.tarjeta-header').forEach(header => {
    header.addEventListener('click', () => {
        const repo = header.closest('.tarjeta-repo');
        if (window.innerWidth <= 768) {
            repo.classList.toggle('expandido');
        }
    });
});
