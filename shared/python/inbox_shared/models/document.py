import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inbox_shared.database import Base
from inbox_shared.enums import DepartmentType, DocumentLabel, DocumentStatus
from inbox_shared.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Document(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "documents"

    originalFilename: Mapped[str] = mapped_column(
        "original_filename",
        String(255),
        nullable=False,
    )

    storedFilename: Mapped[str] = mapped_column(
        "stored_filename",
        String(255),
        nullable=False,
    )

    filePath: Mapped[str] = mapped_column(
        "file_path",
        String(500),
        nullable=False,
    )

    mimeType: Mapped[str] = mapped_column(
        "mime_type",
        String(100),
        nullable=False,
    )

    fileSize: Mapped[int] = mapped_column(
        "file_size",
        BigInteger,
        nullable=False,
    )

    uploadedBy: Mapped[uuid.UUID | None] = mapped_column(
        "uploaded_by",
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    status: Mapped[DocumentStatus] = mapped_column(
        SqlEnum(DocumentStatus, name="document_status_enum"),
        default=DocumentStatus.RECEIVED,
        nullable=False,
        index=True,
    )

    predictedLabel: Mapped[DocumentLabel | None] = mapped_column(
        "predicted_label",
        SqlEnum(DocumentLabel, name="document_predicted_label_enum"),
        nullable=True,
    )

    finalLabel: Mapped[DocumentLabel | None] = mapped_column(
        "final_label",
        SqlEnum(DocumentLabel, name="document_final_label_enum"),
        nullable=True,
    )

    department: Mapped[DepartmentType | None] = mapped_column(
        SqlEnum(DepartmentType, name="document_department_enum"),
        nullable=True,
        index=True,
    )

    confidenceScore: Mapped[float | None] = mapped_column(
        "confidence_score",
        Numeric(5, 4),
        nullable=True,
    )

    reviewedBy: Mapped[uuid.UUID | None] = mapped_column(
        "reviewed_by",
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    reviewedAt: Mapped[datetime | None] = mapped_column(
        "reviewed_at",
        DateTime(timezone=True),
        nullable=True,
    )
    
    deletedBy: Mapped[uuid.UUID | None] = mapped_column(
        "deleted_by",
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    deletedAt: Mapped[datetime | None] = mapped_column(
        "deleted_at",
        DateTime(timezone=True),
        nullable=True,
    )

    uploader = relationship(
        "User",
        back_populates="uploadedDocuments",
        foreign_keys=[uploadedBy],
    )

    reviewer = relationship(
        "User",
        back_populates="reviewedDocuments",
        foreign_keys=[reviewedBy],
    )

    predictions = relationship(
        "DocumentPrediction",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    assignments = relationship(
        "DocumentAssignment",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    auditLogs = relationship(
        "AuditLog",
        back_populates="document",
    )

    incomingEmail = relationship(
        "IncomingEmail",
        back_populates="document",
        uselist=False,
    )
    