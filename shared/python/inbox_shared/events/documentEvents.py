from typing import Any
from uuid import uuid4
from datetime import datetime, timezone

from pydantic import BaseModel, Field


def utcNowIso() -> str:
    return datetime.now(timezone.utc).isoformat()


class BaseEvent(BaseModel):
    eventType: str
    documentId: int
    correlationId: str = Field(default_factory=lambda: str(uuid4()))


class DocumentReceivedEvent(BaseEvent):
    storageKey: str
    sourceType: str
    requiresOcr: bool = False
    receivedAt: str = Field(default_factory=utcNowIso)


class ProcessDocumentRequestedEvent(BaseEvent):
    storageKey: str
    sourceType: str
    requiresOcr: bool = False
    requestedAt: str = Field(default_factory=utcNowIso)


class ProcessDocumentCompletedEvent(BaseEvent):
    predictedLabel: str
    confidence: float
    probabilities: dict[str, float]
    processedAt: str = Field(default_factory=utcNowIso)


class ProcessDocumentFailedEvent(BaseEvent):
    errorCode: str
    errorMessage: str
    failedAt: str = Field(default_factory=utcNowIso)


class DispatchDocumentRequestedEvent(BaseEvent):
    targetDepartment: str
    status: str
    prediction: dict[str, Any]
    requestedAt: str = Field(default_factory=utcNowIso)


class DocumentDispatchedEvent(BaseEvent):
    targetDepartment: str
    status: str
    prediction: dict[str, Any]
    dispatchedAt: str = Field(default_factory=utcNowIso)


class NotificationRequestedEvent(BaseEvent):
    targetDepartment: str
    status: str
    message: str
    createdAt: str = Field(default_factory=utcNowIso)