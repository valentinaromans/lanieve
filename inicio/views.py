from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

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

def ayuda_soporte(request):
    return render(request, 'inicio/ayuda_soporte.html')