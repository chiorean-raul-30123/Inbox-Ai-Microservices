from datetime import datetime, timezone
from uuid import uuid4

from fastapi import UploadFile

from inbox_shared.database import createDbSession
from inbox_shared.enums import AuditAction, DocumentStatus
from inbox_shared.messaging.queueNames import QueueNames
from inbox_shared.repositories import AuditRepository, DocumentRepository
from inbox_shared.services import StorageService

from src.messaging.rabbitPublisher import publishMessage


class ScanInputService:
    def __init__(self) -> None:
        self.storageService = StorageService()
        self.documentRepository = DocumentRepository()
        self.auditRepository = AuditRepository()

    def uploadScan(
        self,
        *,
        file: UploadFile,
        submittedBy: str | None = None,
    ) -> dict:
        db = createDbSession()

        try:
            storedFile = self.storageService.uploadImageFileObject(
                file.file,
                filename=file.filename,
                contentType=file.content_type,
            )

            document = self.documentRepository.create(
                db,
                originalFilename=storedFile["originalFilename"],
                storedFilename=storedFile["storedFilename"],
                filePath=storedFile["objectKey"],
                mimeType=storedFile["mimeType"],
                fileSize=storedFile["fileSize"],
                uploadedBy=None,
                status=DocumentStatus.RECEIVED,
            )

            correlationId = f"scan-{uuid4()}"

            self.auditRepository.create(
                db,
                action=AuditAction.DOCUMENT_RECEIVED,
                documentId=document.id,
                details={
                    "sourceType": "SCAN",
                    "submittedBy": submittedBy,
                    "originalFilename": storedFile["originalFilename"],
                    "storedFilename": storedFile["storedFilename"],
                    "objectKey": storedFile["objectKey"],
                    "mimeType": storedFile["mimeType"],
                    "fileSize": storedFile["fileSize"],
                    "correlationId": correlationId,
                },
            )

            event = {
                "eventType": "DocumentReceived",
                "documentId": str(document.id),
                "storageKey": storedFile["objectKey"],
                "sourceType": "SCAN",
                "requiresOcr": True,
                "receivedAt": datetime.now(timezone.utc).isoformat(),
                "correlationId": correlationId,
            }

            publishMessage(
                queueName=QueueNames.inputScanReceived,
                message=event,
            )

            return {
                "documentId": str(document.id),
                "originalFilename": storedFile["originalFilename"],
                "storageKey": storedFile["objectKey"],
                "status": document.status.value,
                "message": "Scanned document received and queued for OCR processing.",
            }

        finally:
            db.close()