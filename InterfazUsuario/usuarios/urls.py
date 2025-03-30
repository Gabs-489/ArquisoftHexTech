from django.urls import path

from .views import *

urlpatterns = [
    path('interfaz/usuarios', pag_principal),
    path('interfaz/usuarios/historiasClinicas', todas_historias_clinicas),
    path('interfaz/usuarios/HC_paciente', historia_clinica_por_paciente , name = 'HC_paciente'),
]
