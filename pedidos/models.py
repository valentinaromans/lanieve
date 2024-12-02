from django.db import models
from helados.models import Helado

# Tabla de Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=9)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.email} {self.contrasena}"

    def set_password(self, password):
        # Asegúrate de encriptar la contraseña antes de almacenarla
        self.contrasena = password  # Aquí deberías aplicar la encriptación de contraseña si no la has aplicado

class Boleta(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado'),
        ('finalizado', 'Finalizado'),
    ]
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)  # Permite nulos
    estado = models.CharField(max_length=10, choices=ESTADOS)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.estado not in dict(self.ESTADOS):  # Validación estricta
            raise ValueError(f"Estado inválido: {self.estado}. Los estados permitidos son: {', '.join(dict(self.ESTADOS).keys())}.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Boleta #{self.id} - {self.estado}"


# Tabla de BoletaDetalle
class BoletaDetalle(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_boleta = models.ForeignKey(Boleta, null=True, blank=True, on_delete=models.CASCADE)  # Permite nulos
    id_helado = models.ForeignKey(Helado, on_delete=models.CASCADE)
    codigo = models.IntegerField(unique=True)
    cantidad = models.SmallIntegerField()

    def __str__(self):
        return f"Detalle Boleta #{self.id_boleta.id_boleta} - {self.id_helado.nombre}"


# Tabla de Pago
class Pago(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Pago para la Boleta #{self.boleta.id} - Total: {self.total}"
