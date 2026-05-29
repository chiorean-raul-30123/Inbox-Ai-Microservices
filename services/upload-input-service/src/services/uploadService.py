from datetime import datetime, timezone

from fastapi import UploadFile

from inbox_shared.database import createDbSession
from inbox_shared.enums import AuditAction, DocumentStatus
from inbox_shared.messaging.queueNames import QueueNames
from inbox_shared.repositories import AuditRepository, DocumentRepository
from inbox_shared.services import StorageService

from src.messaging.rabbitPublisher import publishMessage
from uuid import uuid4

from inbox_shared.enums import AuditAction, DocumentStatus, EmailProcessingStatus
from inbox_shared.repositories import (
    AuditRepository,
    DocumentRepository,
    IncomingEmailRepository,
)


class UploadService:
    def __init__(self) -> None:
        self.storageService = StorageService()
        self.documentRepository = DocumentRepository()
        self.auditRepository = AuditRepository()
        self.incomingEmailRepository = IncomingEmailRepository()

    def uploadDocument(
        self,
        *,
        file: UploadFile,
        uploadedBy=None,
        senderEmail: str | None = None,
        senderName: str | None = None,
        subject: str | None = None,
        body: str | None = None,
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
            incomingEmail = None

            if senderEmail or senderName or subject or body:
                incomingEmail = self.incomingEmailRepository.create(
                    db,
                    senderEmail=senderEmail or "direct-upload@inbox-ai.local",
                    senderName=senderName or "Direct Upload",
                    subject=subject or storedFile["originalFilename"],
                    body=body,
                    externalMessageId=f"direct-upload-{uuid4()}",   
                    documentId=document.id,
                    processingStatus=EmailProcessingStatus.RECEIVED,
                    receivedAt=datetime.now(timezone.utc),
                )

            event = {
                "eventType": "DocumentReceived",
                "documentId": str(document.id),
                "storageKey": storedFile["objectKey"],
                "sourceType": "UPLOAD",
                "requiresOcr": False,
                "receivedAt": datetime.now(timezone.utc).isoformat(),
                "emailId": str(incomingEmail.id) if incomingEmail else None,
                "senderEmail": senderEmail,
                "subject": subject,
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