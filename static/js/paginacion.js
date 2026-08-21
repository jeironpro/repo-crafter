const TAM_PAGINA = 25;
const contenedorRepos = document.querySelector(".contenedor-repos");

if (contenedorRepos) {
    const reduceMovimiento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const tarjetas = Array.from(contenedorRepos.querySelectorAll(".tarjeta-repo"));
    let paginaActual = 1;

    const nav = document.createElement("nav");
    nav.className = "paginacion";
    nav.setAttribute("aria-label", "Paginación de repositorios");

    const btnPrev = document.createElement("button");
    btnPrev.type = "button";
    btnPrev.className = "paginacion__btn";
    btnPrev.setAttribute("aria-label", "Página anterior");
    btnPrev.innerHTML = '<span class="material-symbols-outlined" aria-hidden="true">chevron_left</span>';

    const nums = document.createElement("span");
    nums.className = "paginacion__nums";
    nums.style.display = "contents";

    const btnNext = document.createElement("button");
    btnNext.type = "button";
    btnNext.className = "paginacion__btn";
    btnNext.setAttribute("aria-label", "Página siguiente");
    btnNext.innerHTML = '<span class="material-symbols-outlined" aria-hidden="true">chevron_right</span>';

    const info = document.createElement("span");
    info.className = "paginacion__info";

    nav.append(btnPrev, nums, btnNext, info);
    contenedorRepos.insertAdjacentElement("afterend", nav);

    function tarjetasVisibles() {
        return tarjetas.filter(tarjeta => !tarjeta.classList.contains("oculta"));
    }

    function ir(pagina, desplazar) {
        paginaActual = pagina;
        render();
        if (desplazar) {
            contenedorRepos.scrollIntoView({
                behavior: reduceMovimiento ? "auto" : "smooth",
                block: "start"
            });
        }
    }

    function renderNumeros(totalPaginas) {
        nums.innerHTML = "";

        const agregarNum = p => {
            const boton = document.createElement("button");
            boton.type = "button";
            boton.className = "paginacion__num";
            boton.textContent = p;
            if (p === paginaActual) boton.setAttribute("aria-current", "page");
            boton.addEventListener("click", () => ir(p, true));
            nums.appendChild(boton);
        };

        const agregarPuntos = () => {
            const puntos = document.createElement("span");
            puntos.className = "paginacion__puntos";
            puntos.setAttribute("aria-hidden", "true");
            puntos.textContent = "…";
            nums.appendChild(puntos);
        };

        let desde = Math.max(2, paginaActual - 2);
        let hasta = Math.min(totalPaginas - 1, paginaActual + 2);

        if (paginaActual <= 3) {
            desde = 2;
            hasta = Math.min(totalPaginas - 1, 5);
        }
        if (paginaActual >= totalPaginas - 2) {
            hasta = totalPaginas - 1;
            desde = Math.max(2, totalPaginas - 4);
        }

        agregarNum(1);
        if (desde > 2) agregarPuntos();
        for (let p = desde; p <= hasta; p++) agregarNum(p);
        if (hasta < totalPaginas - 1) agregarPuntos();
        if (totalPaginas > 1) agregarNum(totalPaginas);
    }

    function render() {
        const visibles = tarjetasVisibles();
        const totalPaginas = Math.max(1, Math.ceil(visibles.length / TAM_PAGINA));
        paginaActual = Math.min(Math.max(1, paginaActual), totalPaginas);

        const inicio = (paginaActual - 1) * TAM_PAGINA;
        const fin = inicio + TAM_PAGINA;

        tarjetas.forEach(tarjeta => { tarjeta.style.display = ""; });
        visibles.forEach((tarjeta, indice) => {
            tarjeta.style.display = (indice >= inicio && indice < fin) ? "" : "none";
        });

        nav.classList.toggle("is-visible", totalPaginas > 1);
        btnPrev.disabled = paginaActual === 1;
        btnNext.disabled = paginaActual === totalPaginas;
        renderNumeros(totalPaginas);
        info.textContent = `${visibles.length ? inicio + 1 : 0}–${Math.min(fin, visibles.length)} de ${visibles.length}`;
    }

    btnPrev.addEventListener("click", () => ir(paginaActual - 1, true));
    btnNext.addEventListener("click", () => ir(paginaActual + 1, true));

    window.actualizarPaginacion = function () {
        paginaActual = 1;
        render();
    };

    render();
}
