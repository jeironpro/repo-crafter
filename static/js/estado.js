window.estadoUrl = (() => {
    function leer() {
        return Object.fromEntries(new URLSearchParams(window.location.search));
    }

    function escribir(cambios, reemplazar = false) {
        const params = new URLSearchParams(window.location.search);

        Object.entries(cambios).forEach(([clave, valor]) => {
            if (valor === null || valor === undefined || valor === "") {
                params.delete(clave);
            } else {
                params.set(clave, String(valor));
            }
        });

        const cadena = params.toString();
        const url = window.location.pathname + (cadena ? `?${cadena}` : "") + window.location.hash;

        if (reemplazar) {
            history.replaceState(null, "", url);
        } else {
            history.pushState(null, "", url);
        }
    }

    return { leer, escribir };
})();
