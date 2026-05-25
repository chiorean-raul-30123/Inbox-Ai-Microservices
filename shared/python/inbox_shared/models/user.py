import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inbox_shared.database import Base
from inbox_shared.models.base import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    fullName: Mapped[str] = mapped_column(
        "full_name",
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    passwordHash: Mapped[str] = mapped_column(
        "password_hash",
        String(255),
        nullable=False,
    )

    isActive: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        default=True,
        nullable=False,
    )

    roleId: Mapped[int] = mapped_column(
        "role_id",
        ForeignKey("roles.id"),
        nullable=False,
    )

    role = relationship(
        "Role",
        back_populates="users",
    )

    uploadedDocuments = relationship(
        "Document",
        back_populates="uploader",
        foreign_keys="Document.uploadedBy",
    )

    reviewedDocuments = relationship(
        "Document",
        back_populates="reviewer",
        foreign_keys="Document.reviewedBy",
    )

    assignedDocuments = relationship(
        "DocumentAssignment",
        back_populates="assignedToUser",
        foreign_keys="DocumentAssignment.assignedToUserId",
    )

    createdAssignments = relationship(
        "DocumentAssignment",
        back_populates="assignedByUser",
        foreign_keys="DocumentAssignment.assignedByUserId",
    )

    auditLogs = relationship(
        "AuditLog",
        back_populates="user",
    )