from django.core.management.base import BaseCommand
from eventos.services.archivo_consumer import iniciar_consumer  # Importa la función corregida

class Command(BaseCommand):
    help = "Inicia el consumidor de RabbitMQ"

    def handle(self, *args, **kwargs):
        iniciar_consumer()
