from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100) 
    apellidos = models.CharField(max_length=100)
    celular = models.IntegerField()
    correo = models.CharField(max_length=200)
    numero_identidad = models.CharField(max_length=12)  
    class Meta:
        abstract = True 

class Paciente(Usuario):
    edad = models.CharField(max_length=3)
    eventos =  models.JSONField(blank=True, default=list)
    E_medicos = models.JSONField(blank=True, default=list)
    
    def __str__(self):
        return '%s %s, Numero de Identidad: %s' % (self.nombre,self.apellidos, self.numero_identidad)