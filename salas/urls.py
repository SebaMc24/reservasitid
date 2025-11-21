from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('sala/<int:pk>/', views.detalle_sala, name='detalle_sala'),
    path('sala/<int:pk>/reservar/', views.reservar, name='reservar'),
]