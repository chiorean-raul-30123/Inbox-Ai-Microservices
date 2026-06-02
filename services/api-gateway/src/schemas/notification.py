from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class NotificationResponse(BaseModel):
    id: UUID
    title: str
    message: str
    status: str | None = None

    targetDepartment: str | None = Field(
        default=None,
        serialization_alias="target_department",
    )

    documentId: UUID | None = Field(
        default=None,
        serialization_alias="document_id",
    )

    correlationId: str | None = Field(
        default=None,
        serialization_alias="correlation_id",
    )

    isRead: bool = Field(
        serialization_alias="is_read",
    )

    createdAt: datetime = Field(
        serialization_alias="created_at",
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class NotificationListResponse(BaseModel):
    notifications: list[NotificationResponse]
    unreadCount: int = Field(serialization_alias="unread_count")

    model_config = ConfigDict(populate_by_name=True)