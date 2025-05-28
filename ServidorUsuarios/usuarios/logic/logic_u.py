"""from ..models import *

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
    return ()  """

from pymongo import MongoClient

from ServidorUsuarios import settings

def get_mongo_client():
    return MongoClient(settings.MONGO_CLI)

def get_paciente_collection():
    client = get_mongo_client()
    db = client.monitoring_db
    return db['pacientes']

def get_resultados_paciente(numero_identidad):
    paciente = get_paciente(numero_identidad) 
    if paciente and 'eventos' in paciente:
        return paciente['eventos']
    return []

def crear_paciente(data):
    col = get_paciente_collection()
    result = col.insert_one(data)
    return str(result.inserted_id)

def get_paciente(numero_identidad):
    col = get_paciente_collection()
    paciente = col.find_one({"numero_identidad": numero_identidad})
    return paciente  # Diccionario o None

def get_pacientes():
    col = get_paciente_collection()
    return list(col.find())

def actualizar_paciente(numero_identidad, nuevos_datos):
    col = get_paciente_collection()
    result = col.update_one(
        {"numero_identidad": numero_identidad},
        {"$set": nuevos_datos}
    )
    return result.modified_count

def eliminar_paciente(numero_identidad):
    col = get_paciente_collection()
    result = col.delete_one({"numero_identidad": numero_identidad})
    return result.deleted_count

