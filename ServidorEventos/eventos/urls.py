from .views import *
from django.urls import path

urlpatterns = [
    path('eventos/', pag_inicial),
    path('eventos/EEG',pag_paciente_examenes),
    path('eventos/EEG/analisis', analisis_eeg,name='analisis_eeg'),
    path('eventos/EEG/resultados', resultados_eeg, name='resultados_eeg')
]