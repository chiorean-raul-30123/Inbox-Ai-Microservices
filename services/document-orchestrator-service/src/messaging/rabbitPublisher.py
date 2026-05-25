import json
import pika


def publishMessage(channel, queueName: str, message: dict):
    channel.basic_publish(
        exchange="",
        routing_key=queueName,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json",
        ),
    )