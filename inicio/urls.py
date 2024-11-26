from django.urls import path
from . import views

app_name = 'inicio'
urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('about-us/', views.sobre_nosotros, name='about_us'),
    path('recomendaciones/', views.recomendaciones, name='recomendaciones'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('codigo/', views.codigo, name='codigo'),
    path('ayuda-soporte/', views.ayuda_soporte, name='ayuda_soporte'),
]   