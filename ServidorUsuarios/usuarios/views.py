import json
from django.http import HttpResponse
from django.shortcuts import render
import hashlib
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

@api_view(['POST'])
def agregar_evento_a_paciente(request):
    data = request.data
    numero_identidad = data.get('numero_identidad')
    nuevo_evento = data.get('nuevo_evento')

    if not numero_identidad or not nuevo_evento:
        return Response(
            {"error": "Faltan datos: 'numero_identidad' o 'nuevo_evento'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    paciente = get_paciente(numero_identidad)
    if not paciente:
        return Response({"error": "Paciente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    hash_cliente = nuevo_evento.get("hash_integridad")
    hash_servidor = generar_hash_evento(nuevo_evento)

    if hash_cliente != hash_servidor:
        return Response(
            {"error": "El hash de integridad no es válido."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not paciente.eventos:
        paciente.eventos = []

    paciente.eventos.append(nuevo_evento)
    paciente.save()

    return Response(
        {"success": True, "mensaje": "Evento agregado correctamente al paciente."},
        status=status.HTTP_200_OK
    )



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
    

def generar_hash_evento(evento):
    cadena = (
        evento.get("fecha_evento", "") +
        evento.get("tipo_evento", "") +
        evento.get("descripcion", "") +
        evento.get("profesional", "")
    )
    return hashlib.sha256(cadena.encode('utf-8')).hexdigest()

