from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from inbox_shared.database import getDb
from inbox_shared.enums import RoleType
from inbox_shared.models import User
from inbox_shared.repositories import AuditRepository

from src.api.deps import requireRoles
from src.schemas.audit import AuditResponse
from src.services.auditService import AuditService


router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
)


def getAuditService():
    return AuditService(
        auditRepository=AuditRepository(),
    )


@router.get(
    "",
    response_model=list[AuditResponse],
    response_model_by_alias=True,
)
def getAuditLogs(
    db: Session = Depends(getDb),
    currentUser: User = Depends(
        requireRoles(RoleType.ADMIN)
    ),
    auditService: AuditService = Depends(
        getAuditService
    ),
):
    logs = auditService.listAuditLogs(db)

    return [
        AuditResponse.model_validate(log)
        for log in logs
    ]