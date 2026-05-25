from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from inbox_shared.database import getDb
from inbox_shared.enums import RoleType
from inbox_shared.models import User
from inbox_shared.repositories import DashboardRepository
from src.api.deps import requireRoles
from src.schemas.dashboard import DashboardSummaryResponse
from src.services.dashboardService import DashboardService


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def getDashboardService() -> DashboardService:
    return DashboardService(
        dashboardRepository=DashboardRepository(),
    )


@router.get("/summary", response_model=DashboardSummaryResponse)
def getDashboardSummary(
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN)),
    dashboardService: DashboardService = Depends(getDashboardService),
):
    return dashboardService.getSummary(db)