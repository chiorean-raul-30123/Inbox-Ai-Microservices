import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from inbox_shared.enums import EmailProcessingStatus
from inbox_shared.models import IncomingEmail


class IncomingEmailRepository:
    def getByExternalMessageId(
        self,
        db: Session,
        externalMessageId: str,
    ) -> IncomingEmail | None:
        stmt = select(IncomingEmail).where(
            IncomingEmail.externalMessageId == externalMessageId
        )

        return db.execute(stmt).scalar_one_or_none()

    def create(
        self,
        db: Session,
        *,
        senderEmail: str,
        senderName: str | None,
        subject: str,
        body: str | None,
        externalMessageId: str,
        documentId: uuid.UUID | None,
        processingStatus: EmailProcessingStatus,
        receivedAt: datetime,
        errorMessage: str | None = None,
    ) -> IncomingEmail:
        incomingEmail = IncomingEmail(
            senderEmail=senderEmail,
            senderName=senderName,
            subject=subject,
            body=body,
            externalMessageId=externalMessageId,
            documentId=documentId,
            processingStatus=processingStatus,
            receivedAt=receivedAt,
            errorMessage=errorMessage,
        )

        db.add(incomingEmail)
        db.commit()
        db.refresh(incomingEmail)

        return incomingEmail

    def save(self, db: Session, incomingEmail: IncomingEmail) -> IncomingEmail:
        db.add(incomingEmail)
        db.commit()
        db.refresh(incomingEmail)

        return incomingEmail