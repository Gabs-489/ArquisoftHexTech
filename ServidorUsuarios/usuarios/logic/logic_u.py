from ..models import *

def get_pacientes():
    queryset = Paciente.objects.all()
    return (queryset)

def get_resultados_paciente(cedula):
    paciente = Paciente.objects.get(cedula=cedula)
    return paciente.eventos

def get_paciente(cedula):
    try:
        usuario = Paciente.objects.get(cedula=cedula)
        return (usuario)
    except:
        usuario = None
        return (usuario)
    
def crear_paciente(form):
    paciente = form.save()
    paciente.save()
    return ()  