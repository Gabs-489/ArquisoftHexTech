import json
from django.shortcuts import render
import hashlib
# Create your views here.

from django.http import HttpResponse
from django.utils.html import escape
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from InterfazUsuario.settings import MICROSERVICIO_EVENTOS_URL

import requests

# Create your views here.

#Cargar todos los examenes
#@login_required
def cargar_eventos(request):
    print("iniciando conexion", MICROSERVICIO_EVENTOS_URL)
    try:
        
        response = requests.get(f"{MICROSERVICIO_EVENTOS_URL}", timeout=20)

        data = response.json() 
        success = data.get("success", False)

        if (success):
            if request.method == 'POST':
                numero_identidad_paciente = request.POST.get('numero_identidad')

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

#@login_required
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

#@login_required
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

            if realizado!= None and realizado['success']: 
                mensaje = "Se envio con exito la solicitud de analisis."
            else:
                mensaje = "No se pudo enviar la solicitud de analisis."
        return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/interfaz/eventos/EEG/analisis";  // Redirigir a la página principal o donde desees
                            </script>
                            """)
    return render(request, 'EEG/archivos.html', context)

#@login_required
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

#@login_required
def nuevo_evento(request):
    paciente_data = request.session.get('paciente_data', None)

    if not paciente_data:
        mensaje = "No se encontró información del paciente."
        return HttpResponse(f"""<script>
                                alert("{mensaje}");
                                window.location.href = "/interfaz/eventos";
                            </script>""")

    if request.method == 'POST':

        integridad_str = ""

        fecha_evento = request.POST.get('fecha_evento')
        tipo_evento = request.POST.get('tipo_evento')
        descripcion = request.POST.get('descripcion')

        if tipo_evento == "consulta":
            causa = request.POST.get('causa')
            hora_inicio = request.POST.get('hora_inicio_consulta')

            if not all([fecha_evento, tipo_evento, causa,hora_inicio]):
                mensaje = "Todos los campos son obligatorios."
                return HttpResponse(f"""<script>
                                        alert("{mensaje}");
                                        window.location.href = "/interfaz/eventos/nuevo";
                                </script>""")
            hora_inicio_num = int(hora_inicio.replace(":", ""))
            integridad_str = f"{fecha_evento}|{tipo_evento}|{descripcion}|{causa}|{hora_inicio_num}"
            

            evento = {"causa":causa, "hora_inicio":hora_inicio_num}

        elif tipo_evento == "cirugia":
            duracion = request.POST.get('duracion')
            hora_inicio = request.POST.get('hora_inicio')
            if not all([fecha_evento, tipo_evento, duracion,hora_inicio]):
                mensaje = "Todos los campos son obligatorios."
                return HttpResponse(f"""<script>
                                        alert("{mensaje}");
                                        window.location.href = "/interfaz/eventos/nuevo";
                                </script>""")
            hora_inicio_num = int(hora_inicio.replace(":", ""))
            integridad_str = f"{fecha_evento}|{tipo_evento}|{descripcion}|{duracion}|{hora_inicio_num}"

            evento = {"duracion":duracion, "hora_inicio":hora_inicio_num}

        elif tipo_evento == "prescripcion":
            medicamento = request.POST.get('medicamento')
            if not all([fecha_evento, tipo_evento, medicamento]):
                mensaje = "Todos los campos son obligatorios."
                return HttpResponse(f"""<script>
                                        alert("{mensaje}");
                                        window.location.href = "/interfaz/eventos/nuevo";
                                </script>""")
            integridad_str = f"{fecha_evento}|{tipo_evento}|{descripcion}|{medicamento}"

            evento = {"medicamento":medicamento}

        elif tipo_evento == "EEG":
            nombre = request.POST.get('nombre')
            peso_archivo = request.POST.get('peso_archivo')
            path = request.POST.get('path')
            if not all([fecha_evento, tipo_evento, nombre, peso_archivo, ]):
                mensaje = "Todos los campos son obligatorios."
                return HttpResponse(f"""<script>
                                        alert("{mensaje}");
                                        window.location.href = "/interfaz/eventos/nuevo";
                                </script>""")
            integridad_str = f"{fecha_evento}|{tipo_evento}|{descripcion}|{nombre}|{peso_archivo}|{path}"

            evento = {"nombre":nombre, "peso_archivo":peso_archivo, "path":path}

        else:
            mensaje = "Debe elegir un tipo de evento."
            return HttpResponse(f"""<script>
                                    alert("{mensaje}");
                                    window.location.href = "/interfaz/eventos/nuevo";
                                </script>""")

        #Para la prueba se pregunta si cambiar el mensaje 
        cambiar = (input("Ingrese 1 si desea cambiar el mensaje: "))
        if cambiar=="1":
            integridad_str="Mensaje modificado"

        print(integridad_str)
        # Crear string de integridad y calcular el hash
        hash_integridad = hashlib.sha256(integridad_str.encode()).hexdigest()

        evento["id_paciente"] = paciente_data['numero_identidad']
        evento["fecha_evento"] = fecha_evento
        evento["tipo_evento"] = tipo_evento
        evento["descripcion"] = descripcion
        evento["hash_integridad"] = hash_integridad
        

        try:
            response = requests.post(f"{MICROSERVICIO_EVENTOS_URL}/crear/nuevo", json=evento, timeout=10)
            resultado = response.json()

            if response.status_code == 200 :
                mensaje = resultado.get("mensaje", "Evento registrado exitosamente.")
                return HttpResponse(f"""<script>
                                        alert("{mensaje}");
                                        window.location.href = "/interfaz/eventos/nuevo";
                                </script>""")

            else:
                mensaje = resultado.get("mensaje", "Error al registrar el evento.")
                print("Error",mensaje)
                mensaje_escapado = escape(mensaje)
                return HttpResponse(f"""<script>
                                        alert("{mensaje_escapado}");
                                        window.location.href = "/interfaz/eventos/nuevo";
                                </script>""")
        except requests.exceptions.RequestException as e:
            mensaje = f"Error de conexión con el microservicio: {str(e)}"
            return HttpResponse(f"""
                    <html>
                        <head>
                            <title>Redirigiendo...</title>
                        </head>
                        <body>
                            <script type="text/javascript">
                                alert("{mensaje}");  // Muestra la ventana emergente
                                setTimeout(function() {{
                                    window.location.href = "/interfaz/eventos/nuevo";
                                }}, 1000);
                            </script>
                        </body>
                    </html>
                """)
    context = {
        "paciente": paciente_data
    }
    return render(request, 'EEG/nuevo_evento.html', context)


def get_evento(request):
    
    return render(request, 'EEG/consultar_evento.html')

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
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('examenes', [])  # Devolver la respuesta en formato JSON
        
        return {"success": False, "error": f"Error en la solicitud: {response.status_code}"}
    
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}


def get_resultados_eeg(eventos):
    try:
        params = {"eventos": json.dumps(eventos)} 
        response = requests.get(f"{MICROSERVICIO_EVENTOS_URL}/EEG/resultados", params=params)
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('examenes', [])   # Devolver la respuesta en formato JSON
        
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

