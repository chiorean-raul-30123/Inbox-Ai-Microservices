import json

from inbox_shared.messaging.queueNames import QueueNames

from src.messaging.rabbitPublisher import publishMessage
from src.services.dispatchService import DispatchService


dispatchService = DispatchService()


def createSenderCallback(channel):
    def callback(ch, method, properties, body):
        try:
            event = json.loads(body.decode("utf-8"))

            print(f"Received dispatch request: {event}")

            dispatchService.handleDispatchDocumentRequested(
                channel=channel,
                event=event,
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as exception:
            try:
                failedEvent = {
                    "eventType": "DocumentDispatchFailed",
                    "documentId": event.get("documentId") if "event" in locals() else None,
                    "sourceService": "document-sender-service",
                    "failedStage": "DOCUMENT_DISPATCH",
                    "errorCode": exception.__class__.__name__,
                    "errorMessage": str(exception),
                    "retryable": True,
                    "retryCount": int(event.get("retryCount", 0)) if "event" in locals() else 0,
                    "correlationId": event.get("correlationId") if "event" in locals() else None,
                }

                publishMessage(
                    channel=channel,
                    queueName=QueueNames.senderDocumentFailed,
                    message=failedEvent,
                )
            finally:
                print(f"Failed to dispatch document: {exception}")
                ch.basic_ack(delivery_tag=method.delivery_tag)

    return callback