from pydantic import BaseModel, Field


class AiThresholdResponse(BaseModel):
    threshold: float


class UpdateAiThresholdRequest(BaseModel):
    threshold: float = Field(..., ge=0.0, le=1.0)