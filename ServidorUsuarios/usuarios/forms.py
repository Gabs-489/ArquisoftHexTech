from django import forms
from .models import *

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nombre',
            'apellidos',
            'celular',
            'correo',
            'numero_identidad'
        ]

        labels = {
            'nombre' : 'Nombre',
            'apellidos' : 'Apellidos',
            'celular' : 'Celular',
            'correo' : 'Correo',
            'numero_identidad' : 'Numero_identidad'
        }
