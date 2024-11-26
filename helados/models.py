from django.db import models

class Helado(models.Model):
    nombre = models.CharField(max_length=100)
    sabor = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre
