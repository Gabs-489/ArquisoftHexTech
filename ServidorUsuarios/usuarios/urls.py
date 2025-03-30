from .views import *
from django.urls import path

urlpatterns = [
    path('usuarios/pacientes',mostrar_pacientes),
    path('usuarios/pacientes/<str:numero_identidad_paciente>', obtener_examenes_paciente, name='obtener_examenes_paciente'),
]