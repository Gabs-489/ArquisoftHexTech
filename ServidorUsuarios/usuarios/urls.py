from .views import *
from django.urls import path

urlpatterns = [
    path('pacientes/'),
    path('pacientes/<str:cedula_paciente>', obtener_examenes_paciente, name='obtener_examenes_paciente'),
]