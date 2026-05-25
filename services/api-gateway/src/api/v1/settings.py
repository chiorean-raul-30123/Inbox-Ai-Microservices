from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from inbox_shared.database import getDb
from inbox_shared.enums import RoleType
from inbox_shared.models import User
from inbox_shared.repositories import SystemSettingsRepository
from inbox_shared.services import SettingsService
from src.api.deps import requireRoles
from src.schemas.settings import AiThresholdResponse, UpdateAiThresholdRequest


router = APIRouter(prefix="/settings", tags=["Settings"])


def getSettingsService() -> SettingsService:
    return SettingsService(
        systemSettingsRepository=SystemSettingsRepository(),
    )


@router.get("/ai-threshold", response_model=AiThresholdResponse)
def getAiThreshold(
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN)),
    settingsService: SettingsService = Depends(getSettingsService),
):
    return AiThresholdResponse(
        threshold=settingsService.getAiThreshold(db),
    )


@router.put("/ai-threshold", response_model=AiThresholdResponse)
def updateAiThreshold(
    request: UpdateAiThresholdRequest,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN)),
    settingsService: SettingsService = Depends(getSettingsService),
):
    threshold = settingsService.updateAiThresholdValue(
        db,
        threshold=request.threshold,
    )

    return AiThresholdResponse(threshold=threshold)