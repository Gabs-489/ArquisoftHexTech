from .views import *
from django.urls import path

urlpatterns = [
    path('eventos/', cargar_examenes),
    path('eventos/<str:numero_identidad_paciente>', examenes_paciente, name='examenes_paciente'),
    path('eventos/EEG/analisis', analisis_eeg,name='analisis_eeg'),
    path('eventos/EEG/analisis/<str:id_examen>',solicitar_analisis),
    path('eventos/EEG/resultados', resultados_eeg, name='resultados_eeg'),
    path('eventos/nuevo', nuevo_evento, name='nuevo_evento')
]