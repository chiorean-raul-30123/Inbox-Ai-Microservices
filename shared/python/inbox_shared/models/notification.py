import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from inbox_shared.database import Base
from inbox_shared.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Notification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "notifications"

    title: Mapped[str] = mapped_column(String(150), nullable=False)

    message: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str | None] = mapped_column(String(80), nullable=True)

    targetDepartment: Mapped[str | None] = mapped_column(
        "target_department",
        String(50),
        nullable=True,
        index=True,
    )

    documentId: Mapped[uuid.UUID | None] = mapped_column(
        "document_id",
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    correlationId: Mapped[str | None] = mapped_column(
        "correlation_id",
        String(255),
        nullable=True,
        index=True,
    )

    isRead: Mapped[bool] = mapped_column(
        "is_read",
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )