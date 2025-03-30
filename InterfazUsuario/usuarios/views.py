from django.http import HttpResponse
from django.shortcuts import render
import requests

from InterfazUsuario.settings import MICROSERVICIO_USUARIOS_URL

# Create your views here.

def pag_principal(request):
    return render(request, 'usuarios/borrador.html')

def todas_historias_clinicas(request):
    response = requests.get(f"{MICROSERVICIO_USUARIOS_URL}/historias_usuario", timeout=20)
    print(response)
    return HttpResponse("Some response text")

def historia_clinica_por_paciente(request):
    numero_identidad = 0
    response = requests.get(f"{MICROSERVICIO_USUARIOS_URL}/historias_usuario/{numero_identidad}", timeout=20)
    print(response)
    return HttpResponse("Some response text")