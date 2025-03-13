from ..models import *

def get_pacientes():
    queryset = Paciente.objects.all()
    return (queryset)

def get_resultados_paciente(numero_identidad):
    paciente = Paciente.objects.get(numero_identidad=numero_identidad)
    return paciente.eventos

def get_paciente(numero_identidad):
    try:
        usuario = Paciente.objects.get(numero_identidad=numero_identidad)
        return (usuario)
    except:
        usuario = None
        return (usuario)
    
def crear_paciente(form):
    paciente = form.save()
    paciente.save()
    return ()  