from rest_framework import serializers
from . import models


class Paciente_serializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'nombre', 'apellidos', 'celular', 'correo', 'numero_identidad','edad','eventos','E_medicos')
        model = models.Paciente