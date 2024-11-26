let preveiwContainer = document.querySelector('.catalogo-prod-preview');
let previewBox = preveiwContainer.querySelectorAll('.catalogo-preview');

document.querySelectorAll('.catalogo-prod-contenedor .catalogo-producto').forEach(product =>{
    product.onclick = () =>{
        preveiwContainer.style.display = 'flex';
        let name = product.getAttribute('data-name');
        previewBox.forEach(preview =>{
            let target = preview.getAttribute('data-target');
            if(name == target){
                preview.classList.add('active')
            }
        });
    };
});

previewBox.forEach(close=>{
    close.querySelector('.fa-times').onclick = () =>{
        close.classList.remove('active');
        preveiwContainer.style.display = 'none';
    }
});