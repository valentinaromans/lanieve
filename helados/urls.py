from django.urls import path
from . import views

app_name = 'helados'

urlpatterns = [
    path('', views.lista_helados, name='lista_helados'),
    path('<int:pk>/', views.detalle_helado, name='detalle_helado'),
    path('nuevo/', views.crear_helado, name='crear_helado'),
    path('<int:pk>/editar/', views.editar_helado, name='editar_helado'),
    path('<int:pk>/eliminar/', views.eliminar_helado, name='eliminar_helado'),
]
