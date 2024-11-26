
let textoOculto_btn = document.getElementById('textoOculto_btn');

let textoOculto = document.getElementById('textoOculto');


textoOculto_btn.addEventListener('click', toggleText);

function toggleText(){
    textoOculto.classList.toggle('about-mostrar');

    if(textoOculto.classList.contains('about-mostrar')){
        textoOculto_btn.innerHTML = 'Ocultar'
    }
    else{
        textoOculto_btn.innerHTML = 'Leer más'
    }
}