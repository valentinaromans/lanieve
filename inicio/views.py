from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from pedidos.models import BoletaDetalle

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


def verificar_codigo(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        try:
            detalle = BoletaDetalle.objects.get(codigo=codigo)
            boleta = detalle.id_boleta
            if boleta.estado == 'pendiente':  # Verifica si está pendiente
                boleta.estado = 'procesado'
                boleta.save()  # Guarda el cambio
                messages.success(request, "El estado de la boleta cambió a 'procesado'.")
            else:
                messages.info(request, f"La boleta ya está en estado '{boleta.estado}'.")
        except BoletaDetalle.DoesNotExist:
            messages.error(request, "El código ingresado no es válido.")
        return redirect('inicio:codigo')  # Redirige a la misma página después de procesar
    return render(request, 'inicio/codigo.html')


def ayuda_soporte(request):
    return render(request, 'inicio/ayuda_soporte.html')