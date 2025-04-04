from django.db import models

# Create your models here.
class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True  

class Examen(Evento):
    nombre = models.CharField(max_length=100) 
    peso_archivo = models.CharField(max_length=100)  
    class Meta:
        abstract = True  

class EEG(Examen):
    path = models.CharField(max_length=500)
    resultado_analisis = models.CharField(max_length=1000)

    def __str__(self):
        return '%s %s %s %s' % (self.id,self.nombre, self.fecha, self.resultado_analisis)
    