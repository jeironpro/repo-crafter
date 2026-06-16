const creaPaginas = document.querySelectorAll('input[name="crea-pagina"]');

creaPaginas.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        checkbox.parentNode.parentNode.submit();
    });
});