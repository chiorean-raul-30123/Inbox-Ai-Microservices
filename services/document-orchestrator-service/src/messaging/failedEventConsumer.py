import json

from src.services.orchestrationService import OrchestrationService


orchestrationService = OrchestrationService()


def createFailedEventCallback(channel):
    def callback(ch, method, properties, body):
        try:
            event = json.loads(body.decode("utf-8"))

            print(f"Received failed event from {method.routing_key}: {event}")

            orchestrationService.handleFailedEvent(
                channel=channel,
                event=event,
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as exception:
            print(f"Failed to handle failed event: {exception}")
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False,
            )

    return callback