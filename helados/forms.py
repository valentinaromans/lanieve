from django import forms
from .models import Helado

class HeladoForm(forms.ModelForm):
    class Meta:
        model = Helado
        fields = ['nombre', 'sabor', 'descripcion', 'precio', 'stock']
