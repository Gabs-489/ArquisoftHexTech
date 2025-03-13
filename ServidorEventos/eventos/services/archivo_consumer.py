import pika
import json
from eventos.logic.logic_analizadorEEG import actualizar_archivo, get_archivo
from eventos.models import EEG  # Asegúrate de importar tu modelo

# Configuración de la conexión a RabbitMQ
rabbit_host = '10.128.0.3'
rabbit_user = 'monitoring_user'
rabbit_password = 'isis2503'
exchange = 'monitoring_prediction'

topic = 'eeg.response'

def callback(ch, method, properties, body):
    payload = json.loads(body.decode('utf8').replace("'", '"'))
    print(payload)
    actualizar_archivo(payload['id'],payload['resultado'])
    print("El resultado se añadio al examen.")

def iniciar_consumer():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='topic')

    queue_name = "monitoring_results"

    channel.queue_declare(queue=queue_name)

    channel.queue_bind(
        exchange=exchange, queue=queue_name, routing_key=topic)

    print('> Esperando resultados de EEG')

    channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
