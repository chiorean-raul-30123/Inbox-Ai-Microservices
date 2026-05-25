import json

from src.services.orchestrationService import OrchestrationService


orchestrationService = OrchestrationService()


def createInputCallback(channel):
    def callback(ch, method, properties, body):
        try:
            event = json.loads(body.decode("utf-8"))

            print(f"Received input event from {method.routing_key}: {event}")

            orchestrationService.handleDocumentReceived(
                channel=channel,
                event=event,
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as exception:
            print(f"Failed to process input event: {exception}")
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False,
            )

    return callback