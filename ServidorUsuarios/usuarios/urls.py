from .views import *
from django.urls import path

urlpatterns = [
    path('pacientes/',mostrar_pacientes),
    path('pacientes/<str:numero_identidad>', obtener_examenes_paciente, name='obtener_examenes_paciente'),
]