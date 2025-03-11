from ..models import EEG

def get_archivos():
    queryset = EEG.objects.all().order_by('-fecha')[:10]
    return (queryset)

def get_resultados():
    queryset = EEG.objects.exclude(resultado_analisis__isnull=True).exclude(resultado_analisis="").order_by('-fecha')[:10]
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

def actualizar_archivo(resultado, archivo_id):
    archivo = get_archivo(id)
    if archivo != None:
        archivo.resultado_analisis = resultado
        archivo.save()
    return ()
    