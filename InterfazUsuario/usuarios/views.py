from django.http import HttpResponse
from django.shortcuts import render
import requests

from InterfazUsuario.settings import MICROSERVICIO_USUARIOS_URL

# Create your views here.

def pag_principal(request):
    return render(request, 'usuarios/pag_principal.html')

def todas_historias_clinicas(request):
    response = requests.get(f"{MICROSERVICIO_USUARIOS_URL}/historias_usuario", timeout=20)
    historias = response.json()
    context = {
        'historiasClinicas' : historias
        }
    return render(request, 'usuarios/HistoriaClinicas.html',context)

def historia_clinica_por_paciente(request):

    if request.method == 'POST':
                numero_identidad_paciente = request.POST.get('numero_identidad')
                if numero_identidad_paciente:
                    response = requests.get(f"{MICROSERVICIO_USUARIOS_URL}/historias_usuario/{numero_identidad_paciente}", timeout=20)
                    if response.status_code != 200:
                        mensaje = "No se encontro un paciente con ese numero de identidad."
                        return HttpResponse(f"""<script>
                                        alert("{mensaje}");
                                        window.location.href = "/interfaz/eventos";  // Redirigir a la página principal o donde desees
                                        </script>
                                        """) 
                    else: 
                        historias = response.json()
                        print(historias)
                        context = {
                                    'historiasClinicas' : historias
                                    }
                        return render(request, 'usuarios/HistoriaClinicasPaciente.html',context)
    
    return render(request, 'usuarios/HistoriaClinicasPaciente.html')