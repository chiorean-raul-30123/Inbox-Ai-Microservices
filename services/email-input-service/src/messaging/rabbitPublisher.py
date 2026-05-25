import json

import pika

from src.messaging.rabbitConnection import createRabbitConnection


def publishMessage(queueName: str, message: dict):
    connection = None

    try:
        connection = createRabbitConnection()
        channel = connection.channel()

        channel.queue_declare(
            queue=queueName,
            durable=True,
        )

        channel.basic_publish(
            exchange="",
            routing_key=queueName,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json",
            ),
        )

    finally:
        if connection is not None and connection.is_open:
            connection.close()