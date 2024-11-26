from django.db import models
from django.contrib.auth.models import User 

class Perfil(models.Model):
    ROLES = (
        ('administrador','Administrador'),
        ('vendedor','Vendedor'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)  # Nuevo campo
    apellido = models.CharField(max_length=50)  # Nuevo campo
    rol=models.CharField(max_length=20,choices=ROLES,default='usuario')
    foto=models.ImageField(upload_to='fotos_perfil',null=True,blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"