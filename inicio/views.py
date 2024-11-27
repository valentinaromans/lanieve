from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from pedidos.models import Boleta

# Create your views here.
def inicio(request):
    return render(request, 'inicio/inicio.html')

def sobre_nosotros(request):
    return render(request, 'inicio/sobre_nosotros.html')

def recomendaciones(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        template = render_to_string('email_template.html', {
            'name': name,
            'email': email,
            'message': message
        })

        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['proyectolanieve@gmail.com']
        )

        email.fail_silently = False
        email.send()

        messages.success(request, 'Se ha enviado tu correo.')
        return redirect('inicio:recomendaciones')
    
    return render(request, 'inicio/recomendaciones.html')


def catalogo(request):
    return render(request, 'inicio/catalogo.html')

def codigo(request):
    return render(request, 'inicio/codigo.html')


from django.shortcuts import render
from pedidos.models import BoletaDetalle, Boleta

def verificar_codigo(request):
    mensaje = ""
    
    if request.method == 'POST':
        codigo = int(request.POST.get('codigo'))
        
        # Buscar el detalle de boleta con el código ingresado
        detalle = BoletaDetalle.objects.filter(codigo=codigo).first()
        
        if detalle:
            boleta = detalle.id_boleta
            if boleta.estado == 'pendiente':
                # Cambiar el estado de la boleta a 'procesado'
                boleta.estado = 'procesado'
                boleta.save()
                mensaje = "El código fue verificado y la boleta ha sido procesada."
            else:
                mensaje = "La boleta ya está procesada o finalizada."
        else:
            mensaje = "Código inválido. Por favor, verifica e intenta nuevamente."
    
    return render(request, 'inicio/codigo.html', {'mensaje': mensaje})



def ayuda_soporte(request):
    return render(request, 'inicio/ayuda_soporte.html')