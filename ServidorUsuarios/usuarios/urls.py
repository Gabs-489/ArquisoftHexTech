from .views import *
from django.urls import path

urlpatterns = [
    path('usuarios/pacientes',mostrar_pacientes),
    path('usuarios/pacientes/new/save', crear_paciente, name='crear_paciente'),
    path('usuarios/pacientes/<str:numero_identidad_paciente>', obtener_examenes_paciente, name='obtener_examenes_paciente'),
    path('usuarios/historias_usuario', obtener_historias_de_pacientes, name='obtener_historias_de_pacientes'),
    path('usuarios/historias_usuario/<str:numero_identidad_paciente>', obtener_historia_de_un_paciente, name='obtener_historia_de_un_paciente'),
]