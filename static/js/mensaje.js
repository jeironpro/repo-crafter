const mensajes = document.querySelectorAll(".mensaje")

mensajes.forEach(mensaje => {
    setTimeout(() => {
        mensaje.style.opacity = '0';
        mensaje.style.transition = 'opacity 0.5s';
        setTimeout(() => mensaje.remove(), 500);
    }, 5000);
});