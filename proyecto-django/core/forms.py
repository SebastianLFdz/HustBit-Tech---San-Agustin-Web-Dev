from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Tu Nombre")
    correo = forms.EmailField(label="Tu Correo Electrónico")
    mensaje = forms.CharField(widget=forms.Textarea, label="¿En qué podemos ayudarte?")