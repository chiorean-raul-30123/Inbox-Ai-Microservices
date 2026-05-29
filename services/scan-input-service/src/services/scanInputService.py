from datetime import datetime, timezone
from uuid import uuid4

from fastapi import UploadFile

from inbox_shared.database import createDbSession
from inbox_shared.enums import AuditAction, DocumentStatus, EmailProcessingStatus
from inbox_shared.messaging.queueNames import QueueNames
from inbox_shared.repositories import (
    AuditRepository,
    DocumentRepository,
    IncomingEmailRepository,
)
from inbox_shared.services import StorageService

from src.messaging.rabbitPublisher import publishMessage


class ScanInputService:
    def __init__(self) -> None:
        self.storageService = StorageService()
        self.documentRepository = DocumentRepository()
        self.auditRepository = AuditRepository()
        self.incomingEmailRepository = IncomingEmailRepository()

    def uploadScan(
        self,
        *,
        file: UploadFile,
        submittedBy: str | None = None,
        senderEmail: str | None = None,
        senderName: str | None = None,
        subject: str | None = None,
        body: str | None = None,
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

            receivedAt = datetime.now(timezone.utc)
            correlationId = f"scan-{uuid4()}"

            incomingEmail = self.incomingEmailRepository.create(
                db,
                senderEmail=senderEmail or "scan-upload@inbox-ai.local",
                senderName=senderName or submittedBy or "Scan Upload",
                subject=subject or storedFile["originalFilename"],
                body=body,
                externalMessageId=correlationId,
                documentId=document.id,
                processingStatus=EmailProcessingStatus.RECEIVED,
                receivedAt=receivedAt,
            )

            self.auditRepository.create(
                db,
                action=AuditAction.DOCUMENT_RECEIVED,
                documentId=document.id,
                details={
                    "sourceType": "SCAN",
                    "submittedBy": submittedBy,
                    "senderEmail": senderEmail,
                    "senderName": senderName,
                    "subject": subject,
                    "incomingEmailId": str(incomingEmail.id),
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
                "emailId": str(incomingEmail.id),
                "senderEmail": incomingEmail.senderEmail,
                "subject": incomingEmail.subject,
                "receivedAt": receivedAt.isoformat(),
                "correlationId": correlationId,
            }

            publishMessage(
                queueName=QueueNames.inputScanReceived,
                message=event,
            )

            return {
                "documentId": str(document.id),
                "emailId": str(incomingEmail.id),
                "originalFilename": storedFile["originalFilename"],
                "storageKey": storedFile["objectKey"],
                "status": document.status.value,
                "message": "Scanned document received and queued for OCR processing.",
            }

        finally:
            db.close()