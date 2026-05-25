import uuid
from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inbox_shared.database import Base
from inbox_shared.enums import AuditAction
from inbox_shared.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class AuditLog(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "audit_logs"

    userId: Mapped[uuid.UUID | None] = mapped_column(
        "user_id",
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    documentId: Mapped[uuid.UUID | None] = mapped_column(
        "document_id",
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    action: Mapped[AuditAction] = mapped_column(
        SqlEnum(AuditAction, name="audit_action_enum"),
        nullable=False,
        index=True,
    )

    details: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="auditLogs",
    )

    document = relationship(
        "Document",
        back_populates="auditLogs",
    )