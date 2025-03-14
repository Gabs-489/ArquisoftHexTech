from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render

from ServidorEventos.settings import MICROSERVICIO_USUARIOS_URL
from eventos.services.archivoProducer import enviar_mensaje
from eventos.services.subir_archivos import listar_archivos
from .logic.logic_analizadorEEG import *

import requests

# Create your views here.

#Cargar todos los examenes
def pag_inicial(request):
    bucket_name = "examenes_eeg"
    listar_archivos(bucket_name)
    if request.method == 'POST':
        numero_identidad_paciente = request.POST.get('numero_identidad')

        if numero_identidad_paciente:
            # Crear el payload con el nombre y la ruta del archivo
            datos = get_examenes_paciente(numero_identidad_paciente)
            if datos == None:
               mensaje = "No se encontro un paciente con ese numero de identidad."
               return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/eventos/";  // Redirigir a la página principal o donde desees
                            </script>
                            """) 
            else: 
                request.session['paciente_data'] = datos
                return redirect('/eventos/EEG')
        else:
            mensaje = f"Error al obtener los exámenes del paciente con el numero de identidad {numero_identidad_paciente}"
            return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/eventos/";  // Redirigir a la página principal o donde desees
                            </script>
                            """) 
    return render(request, 'EEG/pag_principal.html')



def pag_paciente_examenes(request):
    paciente_data = request.session.get('paciente_data', None)

    if not paciente_data:
        mensaje = "No se encontró información del paciente."
        return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/eventos/";  // Redirigir a la página principal o donde desees
                            </script>
                            """)
    context = {
        'paciente' : paciente_data
        }

    if request.method == 'POST':
        return redirect('/eventos/EEG/analisis')
    return render(request, 'EEG/pag_paciente_examenes_EEG.html',context)

def analisis_eeg(request):
    paciente_data = request.session.get('paciente_data', None)
    archivos = get_archivos(paciente_data['eventos'])
    context = {
        'lista_archivos': archivos
    }
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        file_path = request.POST.get('file_path')

        if file_id and file_path:
            # Crear el payload con el nombre y la ruta del archivo
            payload ="{'id': '%s', 'path': '%s'}" % (file_id, file_path)
            enviar_mensaje(payload,file_id)
            mensaje = "Se envio con exito la solicitud de analisis."
        else:
            mensaje = "No se pudo enviar la solicitud de analisis."
        return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/eventos/EEG/analisis";  // Redirigir a la página principal o donde desees
                            </script>
                            """)

    return render(request, 'EEG/archivos.html', context)

def resultados_eeg(request):
    paciente_data = request.session.get('paciente_data', None)
    if not paciente_data:
        mensaje = "No se encontró información del paciente."
        return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/eventos/";  // Redirigir a la página principal o donde desees
                            </script>
                            """)
    
    archivos = get_resultados(paciente_data['eventos'])
    context = {
        'lista_archivos': archivos
    }
    return render(request, 'EEG/resultados.html', context)



def get_examenes_paciente(numero_identidad):
    try:
        response = requests.get(f"{MICROSERVICIO_USUARIOS_URL}/pacientes/{numero_identidad}", timeout=100)
        response.raise_for_status()
        data = response.json()
        print(data)
        if not data:
            print("El paciente con ese numero de documento de identidad, no existe.")
            return None
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los exámenes del paciente con la cedula {numero_identidad}: {e}")
        return None


