import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class RegisterRequest(BaseModel):
    fullName: str = Field(..., min_length=2, max_length=100, alias="full_name")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    roleId: int = Field(alias="role_id")

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


class TokenResponse(BaseModel):
    accessToken: str = Field(serialization_alias="access_token")
    tokenType: str = Field(default="bearer", serialization_alias="token_type")

    model_config = {
        "populate_by_name": True,
    }