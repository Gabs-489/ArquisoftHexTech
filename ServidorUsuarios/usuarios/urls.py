from .views import *
from django.urls import path

urlpatterns = [
    path('usuarios/pacientes',mostrar_pacientes),
    path('usuarios/pacientes/<str:numero_identidad_paciente>', obtener_examenes_paciente, name='obtener_examenes_paciente'),
    path('usuarios/pacientes/nuevo/<str:numero_identidad_paciente>', agregar_evento_a_paciente, name='obtener_examenes_paciente'),
    path('usuarios/historias_usuario', obtener_historias_de_pacientes, name='obtener_historias_de_pacientes'),
    path('usuarios/historias_usuario/<str:numero_identidad_paciente>', obtener_historia_de_un_paciente, name='obtener_historia_de_un_paciente'),
]