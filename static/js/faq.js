document.addEventListener('DOMContentLoaded', () => {
    // Selecciona solo los botones dentro de la clase .faq-button
    const buttons = document.querySelectorAll('.faq-button');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const faq = button.nextElementSibling;  // El <p> de la pregunta
            const icon = button.children[1];  // El ícono de la flecha

            // Alterna las clases para mostrar el contenido y rotar la flecha
            faq.classList.toggle('show');
            icon.classList.toggle('rotate');
        });
    });
});
