from rest_framework import serializers
from . import models


class Examen_serializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'fecha', 'nombre', 'celular', 'peso_archivo', 'path','resultado_analisis')
        model = models.EEG