from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [

    path('registro/', views.RegisterView, name='registro'),
    path('pendientes/', views.pedidos_pendientes, name='pedidospendientes'),
    path('historial/', views.historial_pedidos, name='historialpedidos'),
    path('<int:pk>/', views.detalle_pedido, name='detallepedido'),
    path('confirmar/<int:pedido_id>/', views.confirmar_pedido, name='confirmarpedido'),
    # Rutas para la API de Login y Registro
    path('api/login/', views.LoginView, name='login'),  # Ruta para la autenticación de login
    path('api/register/', views.RegisterView, name='register'),  # Ruta para el registro de usuario
    # API de artículos (Clientes)
    path('api_articulos/', views.api_articulos, name='api_articulos'),
    # API de detalles de artículos (Clientes)
    path('api_articulos_detalle/<int:pk>/', views.api_articulos_detalle, name='api_articulos_detalle'),
]
