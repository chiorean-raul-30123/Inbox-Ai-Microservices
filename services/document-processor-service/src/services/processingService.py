from datetime import datetime, timezone
from pathlib import Path

from inbox_shared.messaging.queueNames import QueueNames
from inbox_shared.services import StorageService

from src.inference.inferencePipeline import InferencePipeline
from src.messaging.rabbitPublisher import publishMessage
from inbox_shared.exceptions import ValidationException


class ProcessingService:
    def __init__(self):
        self.inferencePipeline = InferencePipeline()
        self.StorageService = StorageService()

    def handleProcessDocumentRequested(self, channel, event: dict):
        documentId = event.get("documentId")
        correlationId = event.get("correlationId")
        sourceType = event.get("sourceType")
        requiresOcr = event.get("requiresOcr", False)

        storageKey = event.get("storageKey")
        filePath = event.get("filePath")

        print(
            f"Processing document {documentId}. "
            f"sourceType={sourceType}, requiresOcr={requiresOcr}, "
            f"storageKey={storageKey}, filePath={filePath}"
        )

        localFilePath = self.resolveLocalFilePath(
            storageKey=storageKey,
            filePath=filePath,
        )

        result = self.inferencePipeline.runInference(
            localFilePath,
            requiresOcr=requiresOcr,
        )

        completedEvent = {
            "eventType": "ProcessDocumentCompleted",
            "documentId": documentId,
            "predictedLabel": result["predictedLabel"],
            "confidence": result["confidenceScore"],
            "probabilities": result["probabilities"],
            "modelVersion": result["modelVersion"],
            "processedAt": datetime.now(timezone.utc).isoformat(),
            "correlationId": correlationId,
        }

        publishMessage(
            channel=channel,
            queueName=QueueNames.processorDocumentCompleted,
            message=completedEvent,
        )

        print(
            f"Document {documentId} processed with real AI. "
            f"label={result['predictedLabel']}, "
            f"confidence={result['confidenceScore']}, "
            f"correlationId={correlationId}"
        )

    def resolveLocalFilePath(self, *, storageKey: str | None, filePath: str | None) -> str:
        if filePath and Path(filePath).exists():
            return filePath

        if storageKey:
            return self.StorageService.downloadToTempFile(storageKey)

        raise ValidationException("Either filePath or storageKey must be provided.")