"""from django.db import models

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
    
    def __str__(self):
        return '%s %s, Numero de Identidad: %s' % (self.nombre,self.apellidos, self.numero_identidad)
    """
from mongoengine import Document, EmbeddedDocument, StringField, IntField, ListField, EmbeddedDocumentField

# Modelo base como clase abstracta
class UsuarioBase(EmbeddedDocument):
    nombre = StringField(max_length=100, required=True)
    apellidos = StringField(max_length=100, required=True)
    celular = IntField(required=True)
    correo = StringField(max_length=200, required=True)
    numero_identidad = StringField(max_length=12, required=True)

# Modelo Paciente
class Paciente(Document):
    usuario = EmbeddedDocumentField(UsuarioBase, required=True)
    edad = StringField(max_length=3)
    eventos = ListField()  # puedes especificar tipo si lo deseas, ej: ListField(StringField())

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellidos}, Número de Identidad: {self.usuario.numero_identidad}"
