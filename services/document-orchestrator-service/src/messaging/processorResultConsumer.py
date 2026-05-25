import json

from src.services.orchestrationService import OrchestrationService


orchestrationService = OrchestrationService()


def createProcessorResultCallback(channel):
    def callback(ch, method, properties, body):
        try:
            event = json.loads(body.decode("utf-8"))

            print(f"Received processor result from {method.routing_key}: {event}")

            orchestrationService.handleProcessDocumentCompleted(
                channel=channel,
                event=event,
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as exception:
            print(f"Failed to process processor result: {exception}")
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False,
            )

    return callback