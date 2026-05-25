from datetime import datetime, timezone
from uuid import uuid4
from inbox_shared.messaging.queueNames import QueueNames
from src.messaging.rabbitPublisher import publishMessage
from uuid import UUID

from inbox_shared.database import createDbSession
from inbox_shared.enums import AuditAction, DocumentStatus
from inbox_shared.repositories import AuditRepository, DocumentRepository


class OrchestrationService:
    def __init__(self) -> None:
        self.documentRepository = DocumentRepository()
        self.auditRepository = AuditRepository()

    def handleDocumentReceived(self, channel, event: dict):
        documentId = event.get("documentId")
        storageKey = event.get("storageKey")
        sourceType = event.get("sourceType")
        requiresOcr = event.get("requiresOcr", False)

        correlationId = event.get("correlationId") or str(uuid4())

        processRequest = {
            "eventType": "ProcessDocumentRequested",
            "documentId": documentId,
            "storageKey": storageKey,
            "sourceType": sourceType,
            "requiresOcr": requiresOcr,
            "requestedAt": datetime.now(timezone.utc).isoformat(),
            "correlationId": correlationId,
        }

        publishMessage(
            channel=channel,
            queueName=QueueNames.processorDocumentRequested,
            message=processRequest,
        )

        print(
            f"Document {documentId} sent to processor. "
            f"sourceType={sourceType}, correlationId={correlationId}"
        )

    def handleProcessDocumentCompleted(self, channel, event: dict):
        documentId = event.get("documentId")
        predictedLabel = event.get("predictedLabel")
        confidence = event.get("confidence")
        probabilities = event.get("probabilities", {})
        correlationId = event.get("correlationId")
        modelVersion = event.get("modelVersion", "cnn_v1")

        threshold = 0.75

        if confidence is not None and confidence >= threshold:
            targetDepartment = predictedLabel
            status = "ROUTED"
        else:
            targetDepartment = "NEEDS_REVIEW"
            status = "NEEDS_REVIEW"

        dispatchRequest = {
            "eventType": "DispatchDocumentRequested",
            "documentId": documentId,
            "targetDepartment": targetDepartment,
            "status": status,
            "prediction": {
                "label": predictedLabel,
                "confidence": confidence,
                "probabilities": probabilities,
                "modelVersion": modelVersion,
            },
            "requestedAt": datetime.now(timezone.utc).isoformat(),
            "correlationId": correlationId,
        }

        publishMessage(
            channel=channel,
            queueName=QueueNames.senderDocumentDispatch,
            message=dispatchRequest,
        )

        print(
            f"Dispatch requested for document {documentId}. "
            f"targetDepartment={targetDepartment}, status={status}, "
            f"correlationId={correlationId}"
        )

    def handleFailedEvent(self, channel, event: dict):
        retryCount = int(event.get("retryCount", 0))
        retryable = bool(event.get("retryable", False))
        failedStage = event.get("failedStage")
        documentId = event.get("documentId")
        correlationId = event.get("correlationId")

        maxRetryCount = 3

        if retryable and retryCount < maxRetryCount:
            retryEvent = {
                **event,
                "retryCount": retryCount + 1,
            }

            if failedStage == "DOCUMENT_PROCESSING":
                retryRequest = {
                    "eventType": "ProcessDocumentRequested",
                    "documentId": documentId,
                    "storageKey": event.get("storageKey"),
                    "sourceType": event.get("sourceType", "UNKNOWN"),
                    "requiresOcr": event.get("requiresOcr", False),
                    "retryCount": retryCount + 1,
                    "correlationId": correlationId,
                }

                publishMessage(
                    channel=channel,
                    queueName=QueueNames.processorDocumentRequested,
                    message=retryRequest,
                )

                print(
                    f"Retry scheduled for processor. "
                    f"documentId={documentId}, retryCount={retryCount + 1}"
                )

                return
            
        self.markDocumentAsFailed(event)

        publishMessage(
            channel=channel,
            queueName=QueueNames.deadLetter,
            message=event,
        )

        print(
            f"Event moved to deadLetter.queue. "
            f"documentId={documentId}, failedStage={failedStage}"
        )
        failureNotification = {
            "eventType": "NotificationRequested",
            "documentId": event.get("documentId"),
            "targetDepartment": None,
            "status": "FAILED",
            "message": f"Document failed at stage {event.get('failedStage')}: {event.get('errorMessage')}",
            "createdAt": event.get("occurredAt"),
            "correlationId": event.get("correlationId"),
        }

        publishMessage(
            channel=channel,
            queueName=QueueNames.notification,
            message=failureNotification,
        )

        def markDocumentAsFailed(self, event: dict):
            documentIdValue = event.get("documentId")

            if not documentIdValue:
                print("Failed event has no documentId. Skipping DB status update.")
                return

            db = createDbSession()

            try:
                documentId = UUID(str(documentIdValue))
                document = self.documentRepository.getById(db, documentId)

                if document is None:
                    print(f"Document not found for failed event: {documentId}")
                    return

                failedStage = event.get("failedStage")

                if failedStage == "DOCUMENT_PROCESSING":
                    document.status = DocumentStatus.PROCESSING_FAILED
                    auditAction = AuditAction.DOCUMENT_PROCESSING_FAILED
                elif failedStage == "DOCUMENT_DISPATCH":
                    document.status = DocumentStatus.DISPATCH_FAILED
                    auditAction = AuditAction.DOCUMENT_DISPATCH_FAILED
                else:
                    document.status = DocumentStatus.FAILED
                    auditAction = AuditAction.DOCUMENT_PROCESSING_FAILED

                self.documentRepository.saveDocument(db, document)

                self.auditRepository.create(
                    db,
                    action=auditAction,
                    documentId=document.id,
                    details={
                        "failedStage": event.get("failedStage"),
                        "errorCode": event.get("errorCode"),
                        "errorMessage": event.get("errorMessage"),
                        "retryCount": event.get("retryCount"),
                        "correlationId": event.get("correlationId"),
                    },
                )

                print(
                    f"Document {document.id} marked as {document.status.value} "
                    f"after failedStage={failedStage}"
                )

            finally:
                db.close()