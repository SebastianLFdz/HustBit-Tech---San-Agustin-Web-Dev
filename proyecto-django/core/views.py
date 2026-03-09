from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactoForm
from django.core.mail import EmailMessage

def home(request):
    return render(request, 'index.html')

def contacto(request):
    if request.method == 'POST':
        # 1. Capturamos los datos directamente del HTML manual
        nombre = request.POST.get('nombre')
        email_cliente = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        proyecto = request.POST.get('proyecto')
        mensaje_cuerpo = request.POST.get('mensaje')
        
        # 2. Capturamos el archivo adjunto
        archivo = request.FILES.get('archivo')

        # 3. Preparamos el cuerpo del correo
        contenido = f"""
        Nuevo mensaje de contacto:
        -------------------------
        Cliente: {nombre}
        Correo: {email_cliente}
        Teléfono: {telefono}
        Tipo de Proyecto: {proyecto}

        Mensaje:
        {mensaje_cuerpo}
        """

        # 4. Creamos el objeto de correo
        email = EmailMessage(
            subject=f"Nuevo mensaje de {nombre} - {proyecto}",
            body=contenido,
            from_email=settings.EMAIL_HOST_USER,
            to=['sebaslealfdz@gmail.com'], # Tu correo de destino
            reply_to=[email_cliente]
        )

        # 5. Si el cliente subió un archivo, lo pegamos al correo
        if archivo:
            email.attach(archivo.name, archivo.read(), archivo.content_type)

        # 6. Enviamos
        try:
            email.send(fail_silently=False)
            return redirect('/contacto?exito=1') # Esto activará tu Modal de éxito
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'contacto.html', {'error': True})

    return render(request, 'contacto.html')

def about(request):
    return render(request, 'about.html')

def referencias(request):
    return render(request, 'referencias.html')

def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contra = request.POST.get('password')
        
        # Validación súper simple (puedes mejorarla después con la base de datos de Django)
        if usuario == "admin" and contra == "admin123":
            request.session['is_admin'] = True # Guardamos que ya entró
            return redirect('admin') 
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
            
    return render(request, 'login.html')

def admin(request):
    return render(request, 'admin.html')

