const visibilidades = document.querySelectorAll('input[name="cambia-visibilidad"]');

visibilidades.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        checkbox.parentNode.parentNode.submit();
    });
});