from django.db import models

# Create your models here.
class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True  # Evita que Django cree una tabla para esta clase
