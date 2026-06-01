from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AuditResponse(BaseModel):
    id: UUID

    action: str

    userId: UUID | None = Field(
        default=None,
        serialization_alias="user_id",
    )

    documentId: UUID | None = Field(
        default=None,
        serialization_alias="document_id",
    )

    details: dict | None = None

    createdAt: datetime = Field(
        serialization_alias="created_at",
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )