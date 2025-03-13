import json
from django.http import HttpResponse
from django.shortcuts import render

from ServidorUsuarios.usuarios.serializers import Paciente_serializer

from .logic.logic_u import get_paciente
from .models import Paciente

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

def crear_paciente(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        if get_paciente(data_json)==None:
            paciente = Paciente()
            paciente.nombre = data_json['nombre']
            paciente.celular = data_json['celular']
            paciente.correo = data_json['correo']
            paciente.cedula = data_json['cedula']
            paciente.save()
            return HttpResponse("successfully created measurement")
        else:
            return HttpResponse("unsuccessfully created measurement. Variable or place does not exist")


@api_view(['GET'])
def obtener_examenes_paciente(request, cedula_paciente):
    print("Conexion establecida")
    paciente = get_paciente(cedula_paciente)
    if paciente == None:
        return Response({"error": "Paciente no encontrado"}, status=404)
    serializer = Paciente_serializer(paciente)
    print("Retornando paciente con cedula",cedula_paciente)
    return Response(serializer.data)
