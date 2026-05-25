import json

from inbox_shared.messaging.queueNames import QueueNames

from src.messaging.rabbitPublisher import publishMessage
from src.services.processingService import ProcessingService


processingService = ProcessingService()


def createProcessorCallback(channel):
    def callback(ch, method, properties, body):
        try:
            event = json.loads(body.decode("utf-8"))

            print(f"Received processor request: {event}")

            processingService.handleProcessDocumentRequested(
                channel=channel,
                event=event,
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as exception:
            try:
                failedEvent = {
                    "eventType": "ProcessDocumentFailed",
                    "documentId": event.get("documentId") if "event" in locals() else None,
                    "sourceService": "document-processor-service",
                    "failedStage": "DOCUMENT_PROCESSING",
                    "errorCode": exception.__class__.__name__,
                    "errorMessage": str(exception),
                    "retryable": True,
                    "retryCount": int(event.get("retryCount", 0)) if "event" in locals() else 0,
                    "correlationId": event.get("correlationId") if "event" in locals() else None,
                    "storageKey": event.get("storageKey") if "event" in locals() else None,
                    "sourceType": event.get("sourceType") if "event" in locals() else None,
                    "requiresOcr": event.get("requiresOcr", False) if "event" in locals() else False,
                }

                publishMessage(
                    channel=channel,
                    queueName=QueueNames.processorDocumentFailed,
                    message=failedEvent,
                )
            finally:
                print(f"Failed to process document request: {exception}")
                ch.basic_ack(delivery_tag=method.delivery_tag)

    return callback