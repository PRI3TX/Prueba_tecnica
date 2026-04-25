from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_vehiculos, name='lista_vehiculos'),
    path('toggle/<int:id>/', views.toggle_validado, name='toggle_validado'),
    path('exportar/', views.exportar_csv, name='exportar_csv'),
]
