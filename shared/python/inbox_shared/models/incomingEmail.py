import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inbox_shared.database import Base
from inbox_shared.enums import EmailProcessingStatus
from inbox_shared.models.base import UUIDPrimaryKeyMixin


class IncomingEmail(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "incoming_emails"

    senderEmail: Mapped[str] = mapped_column(
        "sender_email",
        String(255),
        nullable=False,
        index=True,
    )

    senderName: Mapped[str | None] = mapped_column(
        "sender_name",
        String(255),
        nullable=True,
    )

    subject: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    externalMessageId: Mapped[str] = mapped_column(
        "external_message_id",
        String(500),
        unique=True,
        nullable=False,
        index=True,
    )

    documentId: Mapped[uuid.UUID | None] = mapped_column(
        "document_id",
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=True,
        index=True,
    )

    processingStatus: Mapped[EmailProcessingStatus] = mapped_column(
        "processing_status",
        SqlEnum(EmailProcessingStatus, name="email_processing_status_enum"),
        default=EmailProcessingStatus.RECEIVED,
        nullable=False,
        index=True,
    )

    receivedAt: Mapped[datetime] = mapped_column(
        "received_at",
        DateTime(timezone=True),
        nullable=False,
    )

    errorMessage: Mapped[str | None] = mapped_column(
        "error_message",
        Text,
        nullable=True,
    )

    document = relationship(
        "Document",
        back_populates="incomingEmail",
    )