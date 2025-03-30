from django.urls import path

from .views import *

urlpatterns = [
    path('eventos', cargar_eventos),
    path('eventos/EEG',pag_paciente_examenes),
    path('eventos/EEG/analisis', analisis_eeg,name='analisis_eeg'),
    path('eventos/EEG/resultados', resultados_eeg, name='resultados_eeg')
]
