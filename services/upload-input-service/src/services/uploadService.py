from datetime import datetime, timezone

from fastapi import UploadFile

from inbox_shared.database import createDbSession
from inbox_shared.enums import AuditAction, DocumentStatus
from inbox_shared.messaging.queueNames import QueueNames
from inbox_shared.repositories import AuditRepository, DocumentRepository
from inbox_shared.services import StorageService

from src.messaging.rabbitPublisher import publishMessage


class UploadService:
    def __init__(self) -> None:
        self.storageService = StorageService()
        self.documentRepository = DocumentRepository()
        self.auditRepository = AuditRepository()

    def uploadDocument(
        self,
        *,
        file: UploadFile,
        uploadedBy=None,
    ) -> dict:
        db = createDbSession()

        try:
            storedFile = self.storageService.uploadPdfFileObject(
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
                uploadedBy=uploadedBy,
                status=DocumentStatus.RECEIVED,
            )

            self.auditRepository.create(
                db,
                action=AuditAction.DOCUMENT_RECEIVED,
                userId=uploadedBy,
                documentId=document.id,
                details={
                    "originalFilename": storedFile["originalFilename"],
                    "storedFilename": storedFile["storedFilename"],
                    "objectKey": storedFile["objectKey"],
                    "mimeType": storedFile["mimeType"],
                    "fileSize": storedFile["fileSize"],
                    "sourceType": "UPLOAD",
                },
            )

            event = {
                "eventType": "DocumentReceived",
                "documentId": str(document.id),
                "storageKey": storedFile["objectKey"],
                "sourceType": "UPLOAD",
                "requiresOcr": False,
                "receivedAt": datetime.now(timezone.utc).isoformat(),
            }

            publishMessage(
                queueName=QueueNames.inputUploadReceived,
                message=event,
            )

            return {
                "documentId": str(document.id),
                "originalFilename": document.originalFilename,
                "status": document.status.value,
                "storageKey": storedFile["objectKey"],
                "message": "Document received and queued for orchestration.",
            }

        finally:
            db.close()