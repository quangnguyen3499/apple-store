import pika
import json
from django.conf import settings

AMQP_URL = settings.AMQP_URL

params = pika.URLParameters(AMQP_URL)

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="",
        routing_key="main",
        body=json.dumps(body),
        properties=properties,
    )
