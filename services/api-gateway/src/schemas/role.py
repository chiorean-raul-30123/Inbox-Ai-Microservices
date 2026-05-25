from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    createdAt: datetime = Field(serialization_alias="created_at")
    updatedAt: datetime = Field(serialization_alias="updated_at")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )