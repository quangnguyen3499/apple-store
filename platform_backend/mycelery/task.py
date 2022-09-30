from celery import shared_task
import pika
import json
from django.conf import settings

AMQP_URL = settings.AMQP_URL
params = pika.URLParameters(AMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='user', exchange_type='fanout')

def send_mail_active(email, code):
    channel.basic_publish(
        exchange="user",
        routing_key="send_mail_active",
        body=json.dumps({'email': email, 'code': code}),
    )

# @shared_task
# def print_test():
#     channel.queue_declare(queue='queue_1')
#     channel.basic_publish(
#         exchange="exchange_1",
#         routing_key="key_1",
#         body=json.dumps({'username': "Quang"}),
#     )

# @shared_task
# def test_publish():
#     channel.queue_declare(queue='queue_2')
#     channel.basic_publish(
#         exchange="exchange_1",
#         routing_key="key_2",
#         body=json.dumps({"name": "Nguyen"}),
#     )

# def callback(ch, method, properties, body):
#     data = json.loads(body)
#     print(data)
#     if properties.content_type == "customer_list":
#         print(data)

# channel.queue_bind(exchange="exchange_1", queue="hello")
# channel.queue_bind(exchange="exchange_2", queue="main")

# channel.basic_consume(
#     on_message_callback=callback, 
#     queue="hello",
#     auto_ack=True,
# )

# print("Started consuming")

# connection.close()

