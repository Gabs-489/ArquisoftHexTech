from django import forms
from .models import EEG

class EEGForm(forms.ModelForm):
    class Meta:
        model = EEG
        fields = [
            'nombre',
            'path',
            'peso_archivo'
        ]

        labels = {
            'nombre' : 'Nombre',
            'path' : 'Path',
            'peso_archivo' : 'Peso_archivo'
        }
