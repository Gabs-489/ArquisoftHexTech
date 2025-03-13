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
            'cedula'
        ]

        labels = {
            'nombre' : 'Nombre',
            'apellidos' : 'Apellidos',
            'celular' : 'Celular',
            'correo' : 'Correo',
            'cedula' : 'Cedula'
        }
