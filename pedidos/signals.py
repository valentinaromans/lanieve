from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cliente

# Crear un perfil cuando se crea un cliente
@receiver(post_save, sender=Cliente)
def crear_perfil_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(cliente=instance)  # Crea el perfil asociado al cliente

# Guardar el perfil cuando se guarda el cliente
@receiver(post_save, sender=Cliente)
def guardar_perfil_cliente(sender, instance, **kwargs):
    instance.perfil.save()  # Guarda el perfil asociado al cliente
