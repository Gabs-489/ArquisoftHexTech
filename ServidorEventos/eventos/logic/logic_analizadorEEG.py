from ..models import EEG

def get_archivos(id_examenes):
    queryset = EEG.objects.filter(id__in=id_examenes).order_by('-fecha')[:10]
    return (queryset)

def get_resultados(id_examenes):
    queryset = EEG.objects.filter(id__in=id_examenes).exclude(resultado_analisis__isnull=True).exclude(resultado_analisis="").order_by('-fecha')[:10]
    return queryset

def get_archivo(id):
    try:
        archivo = EEG.objects.get(id=id)
        return (archivo)
    except:
        archivo = None
        return (archivo)
    
def crear_archivo(form):
    archivo = form.save()
    archivo.save()
    return ()  

def crear_resultado(form):
    archivo = form.save()
    archivo.save()
    return ()  

def actualizar_archivo(archivo_id,resultado):
    archivo = get_archivo(archivo_id)
    if archivo != None:
        archivo.resultado_analisis = resultado
        archivo.save()
    print(archivo)
    return ()
    