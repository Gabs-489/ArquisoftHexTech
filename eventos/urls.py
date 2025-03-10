from .views import *
from django.urls import path

urlpatterns = [
    path('eventos/EEG', pag_inicial),
    path('eventos/EEG/analisis', analisis_eeg,name='analisis_eeg'),
    path('eventos/EEG/resultados', resultados_eeg, name='resultados_eeg')
]