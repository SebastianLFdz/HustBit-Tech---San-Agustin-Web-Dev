from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactoForm

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Sacamos los datos del formulario
            nombre = form.cleaned_data['nombre']
            email_cliente = form.cleaned_data['correo']
            mensaje_cuerpo = form.cleaned_data['mensaje']

            # Enviamos el correo (Lo que querías lograr)
            send_mail(
                f"Nuevo mensaje de {nombre}",  # Asunto
                f"Cliente: {email_cliente}\n\nMensaje:\n{mensaje_cuerpo}", # Cuerpo
                settings.EMAIL_HOST_USER, # Remitente (tu correo de Brevo/SendGrid)
                ['sebaslealfdz@gmail.com'], # A donde te llegará a ti
                fail_silently=False,
            )
            return render(request, 'core/exito.html') # Una página de "Gracias"
    else:
        form = ContactoForm()
    
    return render(request, 'core/contacto.html', {'form': form})