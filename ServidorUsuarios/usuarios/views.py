import json
from django.http import HttpResponse
from django.shortcuts import render
import requests

from ServidorUsuarios.settings import HISTORIAS_CLINICAS_API
from usuarios.serializers import Paciente_serializer

from .logic.logic_u import get_paciente
from .models import Paciente

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
def mostrar_pacientes(request):
    return HttpResponse(status=204)

def crear_paciente(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        if get_paciente(data_json)==None:
            paciente = Paciente()
            paciente.nombre = data_json['nombre']
            paciente.celular = data_json['celular']
            paciente.correo = data_json['correo']
            paciente.cedula = data_json['numero_identidad']
            paciente.save()
            return HttpResponse("successfully created measurement")
        else:
            return HttpResponse("unsuccessfully created measurement. Variable or place does not exist")



@api_view(['GET'])
def obtener_examenes_paciente(request, numero_identidad_paciente):
    print("Conexion establecida")
    paciente = get_paciente(numero_identidad_paciente)
    if paciente == None:
        return Response({"error": "Paciente no encontrado"}, status=404)
    serializer = Paciente_serializer(paciente)
    print("Retornando paciente con cedula",numero_identidad_paciente)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_historias_de_pacientes(request):
    try: 
        response =  requests.get(f"{HISTORIAS_CLINICAS_API}/api/historias_clinicas/historias/", timeout=20) 

        if response.status_code == 404:
            return Response({"error": "Historias Clinicas no encontradas"}, status=404)
    
        if response.status_code == 200:
            return Response(response.json()) 
        
        return Response({"error": "Error en la obtención de historias clínicas"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def obtener_historia_de_un_paciente(request, numero_identidad_paciente):
    try:
        response = requests.get(f"{HISTORIAS_CLINICAS_API}/api/historias_clinicas/historias/{numero_identidad_paciente}/", timeout=20)

        if response.status_code == 404:
            return Response({"error": "Paciente no encontrado"}, status=404)
        
        if response.status_code == 200:
            return Response(response.json())  
        
        return Response({"error": "Error en la obtención de historias clínicas"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)
