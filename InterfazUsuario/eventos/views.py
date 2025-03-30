import json
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import redirect, render

from InterfazUsuario.settings import MICROSERVICIO_EVENTOS_URL

import requests

# Create your views here.

#Cargar todos los examenes
def cargar_eventos(request):
    print("iniciando conexion", MICROSERVICIO_EVENTOS_URL)
    try:
        
        response = requests.get(f"{MICROSERVICIO_EVENTOS_URL}", timeout=20)

        data = response.json() 
        success = data.get("success", False)
        print(success)

        if (success):
            if request.method == 'POST':
                numero_identidad_paciente = request.POST.get('numero_identidad',)

                if numero_identidad_paciente:
                    datos = get_examenes_paciente(numero_identidad_paciente)
                    if datos == None:
                        mensaje = "No se encontro un paciente con ese numero de identidad."
                        return HttpResponse(f"""<script>
                                        alert("{mensaje}");
                                        window.location.href = "/interfaz/eventos";  // Redirigir a la página principal o donde desees
                                    </script>
                                    """) 
                    else: 
                        request.session['paciente_data'] = datos
                        return redirect('/interfaz/eventos/EEG')
                else:
                    mensaje = f"Error al obtener los exámenes del paciente con el numero de identidad {numero_identidad_paciente}"
                    return HttpResponse(f"""<script>
                                        alert("{mensaje}");
                                        window.location.href = "/interfaz/eventos";  // Redirigir a la página principal o donde desees
                                    </script>
                                    """) 
            return render(request, 'EEG/pag_principal.html')
        else:
            mensaje = f"Error al cargar los eventos desde la base de datos"
            return HttpResponse(f"""<script>
                                        alert("{mensaje}");
                                        window.location.href = "/";  // Redirigir a la página principal o donde desees
                                    </script>
                                    """) 
    except requests.exceptions.RequestException as e:
        # Handle exceptions like timeouts, connection errors, etc.
        mensaje = f"Error al realizar la solicitud: {str(e)}"
        return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/";  // Redirigir a la página principal o donde desees
                            </script>
                            """)

def pag_paciente_examenes(request):
    paciente_data = request.session.get('paciente_data', None)

    if not paciente_data:
        mensaje = "No se encontró información del paciente."
        return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/interfaz/eventos";  // Redirigir a la página principal o donde desees
                            </script>
                            """)
    context = {
        'paciente' : paciente_data
        }

    if request.method == 'POST':
        return redirect('/interfaz/eventos/EEG/analisis')
    return render(request, 'EEG/pag_paciente_examenes_EEG.html',context)


def analisis_eeg(request):
    paciente_data = request.session.get('paciente_data', None)
    archivos = get_examenes_eeg(paciente_data['eventos'])
    context = {
        'lista_archivos': archivos
    }
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        file_path = request.POST.get('file_path')

        if file_id and file_path:
            # Hacer que el servidor envie el mensaje con el id del archivo
            realizado = solicitar_analisis(file_id)

            if realizado['success']: 
                mensaje = "Se envio con exito la solicitud de analisis."
            else:
                mensaje = "No se pudo enviar la solicitud de analisis."
        return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/interfaz/eventos/EEG/analisis";  // Redirigir a la página principal o donde desees
                            </script>
                            """)
    return render(request, 'EEG/archivos.html', context)


def resultados_eeg(request):
    paciente_data = request.session.get('paciente_data', None)
    if not paciente_data:
        mensaje = "No se encontró información del paciente."
        return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/interfaz/eventos";  // Redirigir a la página principal o donde desees
                            </script>
                            """)
    
    archivos = get_resultados_eeg(paciente_data['eventos'])
    context = {
        'lista_archivos': archivos
    }
    return render(request, 'EEG/resultados.html', context)


def get_examenes_paciente(numero_identidad):
    try:
        response = requests.get(f"{MICROSERVICIO_EVENTOS_URL}/{numero_identidad}", timeout=100)
        response.raise_for_status()
        data = response.json()
        print(data)
        if not data['success']:
            print("El paciente con ese número de documento de identidad no existe.")
            return None
        
        return data['data']
    
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Paciente con cédula {numero_identidad} no encontrado. Error 404.")
        elif response.status_code == 400:
            print(f"Solicitud incorrecta para la cédula {numero_identidad}. Error 400.")
        else:
            print(f"Error HTTP al obtener los exámenes del paciente con la cédula {numero_identidad}: {http_err}")
        return None
    
    except requests.exceptions.RequestException as err:
        print(f"Error de red o conexión al obtener los exámenes del paciente con la cédula {numero_identidad}: {err}")
        return None


def get_examenes_eeg(eventos):
    try:
        params = {"eventos": json.dumps(eventos)} 
        response = requests.get(f"{MICROSERVICIO_EVENTOS_URL}/EEG/analisis", params=params)
        print(response)
        if response.status_code == 200:
            return response.json()  # Devolver la respuesta en formato JSON
        
        return {"success": False, "error": f"Error en la solicitud: {response.status_code}"}
    
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}


def get_resultados_eeg(eventos):
    try:
        params = {"eventos": json.dumps(eventos)} 
        response = requests.get(f"{MICROSERVICIO_EVENTOS_URL}/EEG/resultados", params=params)
        if response.status_code == 200:
            return response.json()  # Devolver la respuesta en formato JSON
        
        return {"success": False, "error": f"Error en la solicitud: {response.status_code}"}
    
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}


def solicitar_analisis(id_evento):
    try:
        response = requests.post(f"{MICROSERVICIO_EVENTOS_URL}/EEG/analisis/{id_evento}", timeout=100)
        response.raise_for_status()
        return response.json()  # Devolver la respuesta en formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud de analisis del examen {id_evento}: {e}")
        return None