from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests

from InterfazUsuario.settings import MICROSERVICIO_USUARIOS_URL, MICROSERVICIO_MONITOREO_URL

# Create your views here.

#@login_required
def pag_principal(request):
    return render(request, 'usuarios/pag_principal.html')

#@login_required
def todas_historias_clinicas(request):
    try:
        response = requests.get(f"{MICROSERVICIO_USUARIOS_URL}/historias_usuario", timeout=20)
        response.raise_for_status()  # lanza error si status != 200
        historias = response.json()
        
        if not historias:  # Si la lista está vacía
            mensaje = "No hay historias clínicas disponibles. Puede ser una falla del servidor de Usuarios."
            return HttpResponse(f"""<script>
                                    alert("{mensaje}");
                                    window.location.href = "/interfaz/usuarios";  // Redirigir a la página principal o donde desees
                                </script>
                                """)
 
        context = {
            'historiasClinicas': historias
        }
        return render(request, 'usuarios/HistoriaClinicas.html', context)

    except Exception as e:
        mensaje = f"Error al obtener historias clínicas: {str(e)}"
        print(mensaje)
        if mensaje == "Error al obtener historias clínicas: 503 Server Error: Service Temporarily Unavailable for url: http://10.128.0.8:8000/usuarios/historias_usuario":
            print("funcion mandar mensaje")
            mandar_mensaje_advertencia()
             
        return HttpResponse(f"""<script>
                                    alert("{mensaje}");
                                    window.location.href = "/interfaz/usuarios";  // Redirigir a la página principal o donde desees
                                </script>
                                """)

#@login_required
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

def mandar_mensaje_advertencia():
    #Llamar al servidor de monitoreo
    response = requests.get(f"{MICROSERVICIO_MONITOREO_URL}/errorUsuarios", timeout=20)
    response.raise_for_status()  # lanza error si status != 200
    print("Mensaje enviado Correctamente")
