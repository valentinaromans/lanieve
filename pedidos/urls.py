from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('pendientes/', views.pedidos_pendientes, name='pedidospendientes'),
    path('historial/', views.historial_pedidos, name='historialpedidos'),
    path('<int:pk>/', views.detalle_pedido, name='detallepedido'),
    path('confirmar/<int:pedido_id>/', views.confirmar_pedido, name='confirmarpedido'),


    path('login/', views.LoginView, name='login'),  # Mantener solo esta línea


    #path('logout/', views.logout_view, name='logout'),

    path('api_articulos/', views.api_articulos, name='api_articulos'),
    path('api_articulos_detalle/<int:pk>/', views.api_articulos_detalle, name='api_articulos_detalle'),
]


