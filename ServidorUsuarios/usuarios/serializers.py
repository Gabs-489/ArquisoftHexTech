from rest_framework import serializers
from . import models


class Paciente_serializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'nombre', 'apellidos', 'celular', 'correo', 'cedula','edad','eventos')
        model = models.Paciente