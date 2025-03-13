from django import forms
from .models import *

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nombre',
            'celular',
            'correo',
            'cedula'
        ]

        labels = {
            'nombre' : 'Nombre',
            'celular' : 'Celular',
            'correo' : 'Correo',
            'cedula' : 'Cedula'
        }
