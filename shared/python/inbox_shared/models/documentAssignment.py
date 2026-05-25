import uuid

from sqlalchemy import ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inbox_shared.database import Base
from inbox_shared.enums import AssignmentType, DepartmentType
from inbox_shared.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class DocumentAssignment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "document_assignments"

    documentId: Mapped[uuid.UUID] = mapped_column(
        "document_id",
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    department: Mapped[DepartmentType] = mapped_column(
        SqlEnum(DepartmentType, name="assignment_department_enum"),
        nullable=False,
        index=True,
    )

    assignedToUserId: Mapped[uuid.UUID | None] = mapped_column(
        "assigned_to_user_id",
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    assignedByUserId: Mapped[uuid.UUID | None] = mapped_column(
        "assigned_by_user_id",
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    assignmentType: Mapped[AssignmentType] = mapped_column(
        "assignment_type",
        SqlEnum(AssignmentType, name="assignment_type_enum"),
        nullable=False,
    )

    document = relationship(
        "Document",
        back_populates="assignments",
    )

    assignedToUser = relationship(
        "User",
        back_populates="assignedDocuments",
        foreign_keys=[assignedToUserId],
    )

    assignedByUser = relationship(
        "User",
        back_populates="createdAssignments",
        foreign_keys=[assignedByUserId],
    )