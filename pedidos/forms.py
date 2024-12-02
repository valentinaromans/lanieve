from django import forms
from .models import Cliente

class RegistroForm(forms.ModelForm):

    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    nombre = forms.CharField(max_length=50, label='Nombre')
    apellido = forms.CharField(max_length=50, label='Apellido')
    telefono = forms.CharField(max_length=9, label='Teléfono')
    email = forms.EmailField(label='Correo Electrónico')

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email', 'contrasena']

