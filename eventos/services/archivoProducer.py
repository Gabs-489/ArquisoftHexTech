import time
import pika


rabbit_host = '10.128.0.3'
rabbit_user = 'monitoring_user'
rabbit_password = 'isis2503'
exchange = 'monitoring_prediction'

topic = 'eeg.request'

def enviar_mensaje(payload,nombre):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='topic')

    channel.queue_declare(queue="monitoring_prediction")

    channel.queue_bind(exchange=exchange, queue="monitoring_prediction", routing_key=topic)

    print('> Enviando el archivo')

    channel.basic_publish(exchange=exchange,
                        routing_key=topic, body=payload)
    print("Se envio el archivo:", nombre)

    time.sleep(10)

    connection.close()