from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.schemas.role import RoleResponse


class UserResponse(BaseModel):
    id: UUID
    fullName: str = Field(serialization_alias="full_name")
    email: EmailStr
    isActive: bool = Field(serialization_alias="is_active")
    role: RoleResponse
    createdAt: datetime = Field(serialization_alias="created_at")
    updatedAt: datetime = Field(serialization_alias="updated_at")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserSummaryResponse(BaseModel):
    id: UUID
    fullName: str = Field(serialization_alias="full_name")
    email: EmailStr
    isActive: bool = Field(serialization_alias="is_active")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)