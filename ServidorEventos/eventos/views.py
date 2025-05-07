import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render

from .serializers import Examen_serializer
from ServidorEventos.settings import MICROSERVICIO_USUARIOS_URL
from eventos.services.archivoProducer import enviar_mensaje
from eventos.services.subir_archivos import listar_archivos
from .logic.logic_analizadorEEG import *

import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

#Cargar todos los examenes
@api_view(['GET'])
def cargar_examenes(request):
    print("Conexion establecida")
    bucket_name = "examenes_eeg"
    try:
        listar_archivos(bucket_name)
        success = True 
    except Exception as e:
        success = False  
        print(f"Error al cargar los exámenes: {e}")  
    return Response({"success": success})

@api_view(['GET'])
def examenes_paciente(request, numero_identidad_paciente):
    if numero_identidad_paciente:
        # Crear el payload con el nombre y la ruta del archivo
        datos = get_examenes_paciente(numero_identidad_paciente)
        if datos == None:
            return Response({
                "success": False,
                "message": "No se encontró un paciente con ese número de identidad."
            }, status=404)
        
        return Response({
            "success": True,
            "data": datos
        }, status=200)
    
    else:
        return Response({
            "success": False,
            "message": "Número de identidad no proporcionado."
        }, status=400)


#Solicitar el analisis
@api_view(['POST'])
def solicitar_analisis(request,id_examen):
    examen = get_archivo(id_examen)
    if examen == None:
        return Response({"success": False, "error": "No se encontro el examen"}, status=404)
    
    payload ="{'id': '%s', 'path': '%s'}" % (examen.id, examen.path)
    enviado = enviar_mensaje(payload,examen.id)

    if enviado: 
        mensaje = "Se envio con exito la solicitud de analisis."
        return Response({"success": True, "mensaje":mensaje},status=200)
    else:
        return Response({"success": False},status=500)


@api_view(['GET'])
def analisis_eeg(request):
    eventos_json = request.GET.get("eventos", "[]")  # Obtener la lista de exámenes en JSON
    print("Iniciando busqueda de examenes")
    try:
        eventos = json.loads(eventos_json)  # Convertir a lista de Python
        if isinstance(eventos, list) and all(isinstance(num, int) for num in eventos):
            archivos = get_archivos(eventos)  # Obtener los exámenes desde la BD
            serializer = Examen_serializer(archivos, many=True)
            return Response({"success": True, "examenes": serializer.data})  # Serializar el QuerySet
        else:
            return Response({"success": False, "error": "Formato incorrecto"}, status=400)
    except json.JSONDecodeError:
        return Response({"success": False, "error": "JSON inválido"}, status=400)   
    

@api_view(['GET'])
def resultados_eeg(request):
    eventos_json = request.GET.get("eventos", "[]")  # Obtener la lista de exámenes en JSON
    try:
        eventos = json.loads(eventos_json)  # Convertir a lista de Python
        if isinstance(eventos, list) and all(isinstance(num, int) for num in eventos):
            archivos = get_resultados(eventos)  # Obtener los exámenes desde la BD
            return Response({"success": True, "examenes": list(archivos.values())})  # Serializar el QuerySet
        else:
            return Response({"success": False, "error": "Formato incorrecto"}, status=400)
    except json.JSONDecodeError:
        return Response({"success": False, "error": "JSON inválido"}, status=400)   


#Generar un nuevo evento
@api_view(['GET', 'POST'])
def nuevo_evento(request):
    print("Conexion para crear evento")
    hash_integridad = request.data.get("hash_integridad")

    if not hash_integridad:
        return Response({"error": "Falta el hash de integridad"}, status=400)

    # Procesar evento...
    return Response({"mensaje": "Evento recibido correctamente", "hash": hash_integridad})

def get_examenes_paciente(numero_identidad):
    try:
        print("Inicia busqueda Paciente")
        response = requests.get(f"{MICROSERVICIO_USUARIOS_URL}/pacientes/{numero_identidad}", timeout=100)
        response.raise_for_status()
        data = response.json()
        if not data:
            print("El paciente con ese numero de documento de identidad, no existe.")
            return None
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los exámenes del paciente con la cedula {numero_identidad}: {e}")
        return None


