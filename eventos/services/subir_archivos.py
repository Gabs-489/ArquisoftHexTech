from google.cloud import storage

from eventos.forms import EEGForm
from eventos.logic.logic_analizadorEEG import crear_archivo
from eventos.models import EEG
from django.core.files.storage import default_storage

def listar_archivos(bucket_name):
    """ Lista los archivos en GCS con su nombre y URL. """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    archivos = []
    for blob in bucket.list_blobs():
        nombre_archivo = blob.name
        url_archivo = f"gs://{bucket_name}/{nombre_archivo}"
        peso_archivo = blob.size
        
        # Verificar si ya existe en la BD para evitar duplicados
        if not EGG.objects.filter(path=url_archivo).exists():
            form = EEGForm({'nombre': nombre_archivo, 'path': url_archivo, 'peso_archivo':peso_archivo})
            
            if form.is_valid():
                crear_archivo(form)  # Guardar en la base de datos
                archivos.append(nombre_archivo)
    
    print("Se cargaron",len(archivos),"Archivos de EEG")