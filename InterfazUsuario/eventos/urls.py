from django.urls import path

from .views import *

urlpatterns = [
    path('interfaz/eventos', cargar_eventos),
    path('interfaz/eventos/EEG',pag_paciente_examenes),
    path('interfaz/eventos/EEG/analisis', analisis_eeg,name='analisis_eeg'),
    path('interfaz/eventos/EEG/resultados', resultados_eeg, name='resultados_eeg')
]
