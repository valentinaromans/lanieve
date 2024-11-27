from django.db import models
from helados.models import Helado  # Asegúrate de importar correctamente

class Boleta(models.Model):
    cliente_id = models.IntegerField()  # Relacionado con 'id' de la tabla cliente
    helados = models.ManyToManyField(Helado, related_name="boletas")
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('procesado', 'Procesado'), ('finalizado', 'Finalizado')],
    )
    fecha_hora = models.DateTimeField(auto_now_add=True)
    codigo = models.IntegerField(unique=True)

    def __str__(self):
        return f"Boleta {self.codigo} - Cliente {self.cliente_id}"
