import pika

from src.core.config import settings


def createRabbitConnection():
    credentials = pika.PlainCredentials(
        settings.rabbitUser,
        settings.rabbitPassword,
    )

    parameters = pika.ConnectionParameters(
        host=settings.rabbitHost,
        port=settings.rabbitPort,
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300,
    )

    return pika.BlockingConnection(parameters)