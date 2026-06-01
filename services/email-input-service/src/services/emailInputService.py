from datetime import datetime, timezone
from uuid import uuid4

from fastapi import UploadFile

from inbox_shared.database import createDbSession
from inbox_shared.enums import AuditAction, DocumentStatus, EmailProcessingStatus
from inbox_shared.exceptions import MalwareDetectedException, SecurityScanException
from inbox_shared.messaging.queueNames import QueueNames
from inbox_shared.repositories import (
    AuditRepository,
    DocumentRepository,
    IncomingEmailRepository,
)
from inbox_shared.services import StorageService

from src.messaging.rabbitPublisher import publishMessage
from typing import Any
from src.services.mailpitClient import MailpitClient


class EmailInputService:
    def __init__(self) -> None:
        self.storageService = StorageService()
        self.documentRepository = DocumentRepository()
        self.auditRepository = AuditRepository()
        self.incomingEmailRepository = IncomingEmailRepository()
        self.mailpitClient = MailpitClient()

    def processSimulatedEmail(
        self,
        *,
        senderEmail: str,
        senderName: str | None,
        subject: str,
        body: str | None,
        attachments: list[UploadFile],
    ) -> dict:
        db = createDbSession()

        uploadedDocuments = []
        failedAttachments = []

        externalMessageBaseId = f"simulated-{uuid4()}"
        receivedAt = datetime.now(timezone.utc)

        try:
            for index, attachment in enumerate(attachments):
                externalMessageId = f"{externalMessageBaseId}-attachment-{index + 1}"

                try:
                    storedFile = self.storageService.uploadPdfFileObject(
                        attachment.file,
                        filename=attachment.filename,
                        contentType=attachment.content_type,
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

                    incomingEmail = self.incomingEmailRepository.create(
                        db,
                        senderEmail=senderEmail,
                        senderName=senderName,
                        subject=subject,
                        body=body,
                        externalMessageId=externalMessageId,
                        documentId=document.id,
                        processingStatus=EmailProcessingStatus.RECEIVED,
                        receivedAt=receivedAt,
                    )

                    self.auditRepository.create(
                        db,
                        action=AuditAction.DOCUMENT_RECEIVED,
                        documentId=document.id,
                        details={
                            "sourceType": "EMAIL",
                            "senderEmail": senderEmail,
                            "senderName": senderName,
                            "subject": subject,
                            "externalMessageId": externalMessageId,
                            "originalFilename": storedFile["originalFilename"],
                            "storedFilename": storedFile["storedFilename"],
                            "objectKey": storedFile["objectKey"],
                            "mimeType": storedFile["mimeType"],
                            "fileSize": storedFile["fileSize"],
                        },
                    )

                    event = {
                        "eventType": "DocumentReceived",
                        "documentId": str(document.id),
                        "storageKey": storedFile["objectKey"],
                        "sourceType": "EMAIL",
                        "requiresOcr": False,
                        "emailId": str(incomingEmail.id),
                        "senderEmail": senderEmail,
                        "subject": subject,
                        "receivedAt": receivedAt.isoformat(),
                        "correlationId": externalMessageId,
                    }

                    publishMessage(
                        queueName=QueueNames.inputEmailReceived,
                        message=event,
                    )

                    uploadedDocuments.append(
                        {
                            "documentId": str(document.id),
                            "emailId": str(incomingEmail.id),
                            "originalFilename": storedFile["originalFilename"],
                            "storageKey": storedFile["objectKey"],
                            "status": document.status.value,
                            "message": "Email attachment received and queued.",
                        }
                    )

                except MalwareDetectedException:
                    raise

                except SecurityScanException:
                    raise

                except Exception as exception:
                    failedAttachments.append(
                        {
                            "originalFilename": attachment.filename or "unknown",
                            "success": False,
                            "message": str(exception),
                        }
                    )

            return {
                "externalMessageBaseId": externalMessageBaseId,
                "senderEmail": senderEmail,
                "subject": subject,
                "uploadedDocuments": uploadedDocuments,
                "failedAttachments": failedAttachments,
            }

        finally:
            db.close()
    
    def processMailpitWebhook(self, *, messageId: str) -> dict:
        message = self.mailpitClient.getMessage(messageId)

        fromData = message.get("From") or {}
        senderEmail = fromData.get("Address") or "unknown@local.test"
        senderName = fromData.get("Name")

        subject = message.get("Subject") or "No subject"
        body = (
            message.get("Text")
            or message.get("HTML")
            or ""
        )

        attachments = []

        for attachment in message.get("Attachments") or []:
            partId = (
                attachment.get("PartID")
                or attachment.get("PartId")
                or attachment.get("partId")
            )

            filename = attachment.get("FileName") or attachment.get("Filename") or "attachment.pdf"
            contentType = attachment.get("ContentType") or "application/pdf"

            if not partId:
                continue

            attachments.append(
                self.mailpitClient.getAttachmentFile(
                    messageId=messageId,
                    partId=partId,
                    filename=filename,
                    contentType=contentType,
                )
            )

        return self.processSimulatedEmail(
            senderEmail=senderEmail,
            senderName=senderName,
            subject=subject,
            body=body,
            attachments=attachments,
        )