from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


def utcNowIso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ErrorEvent(BaseModel):
    eventType: str
    documentId: str | None = None
    sourceService: str
    failedStage: str
    errorCode: str
    errorMessage: str
    retryable: bool = False
    retryCount: int = 0
    occurredAt: str = Field(default_factory=utcNowIso)
    correlationId: str = Field(default_factory=lambda: str(uuid4()))