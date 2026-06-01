from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
import re

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


class CreateUserRequest(BaseModel):
    fullName: str = Field(..., min_length=2, max_length=100, alias="full_name")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    roleId: int = Field(alias="role_id")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("password")
    @classmethod
    def validatePassword(cls, value: str) -> str:
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[@$!%*?&]", value):
            raise ValueError(
                "Password must contain at least one special character (@$!%*?&)"
            )

        return value
    
class ChangePasswordRequest(BaseModel):
    currentPassword: str = Field(..., min_length=8, max_length=128, alias="current_password")
    newPassword: str = Field(..., min_length=8, max_length=128, alias="new_password")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("newPassword")
    @classmethod
    def validatePassword(cls, value: str) -> str:
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[@$!%*?&]", value):
            raise ValueError(
                "Password must contain at least one special character (@$!%*?&)"
            )

        return value