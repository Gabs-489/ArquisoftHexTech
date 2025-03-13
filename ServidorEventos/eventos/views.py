from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render

from ServidorEventos.ServidorEventos.settings import MICROSERVICIO_USUARIOS_URL
from eventos.services.archivoProducer import enviar_mensaje
from eventos.services.subir_archivos import listar_archivos
from .logic.logic_analizadorEEG import *

import requests

# Create your views here.

def pag_inicial(request):
    if request.method == 'POST':
        bucket_name = "examenes_eeg"
        listar_archivos(bucket_name)
        return redirect('/eventos/EEG/analisis')
    return render(request, 'EEG/pag_principal.html')

def analisis_eeg(request):
    archivos = get_archivos()
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
    archivos = get_resultados()
    context = {
        'lista_archivos': archivos
    }
    return render(request, 'EEG/resultados.html', context)



def get_examenes_paciente(cedula_paciente):
    try:
        response = requests.get(f"{MICROSERVICIO_USUARIOS_URL}/{cedula_paciente}", timeout=5)
        response.raise_for_status()
        data = response.json()
        if not data:
            print("El paciente con ese numero de documento de identidad, no existe.")
            return None
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los exámenes del paciente con la cedula {cedula_paciente}: {e}")
        return None


