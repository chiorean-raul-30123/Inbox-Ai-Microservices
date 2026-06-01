from sqlalchemy.orm import Session

from inbox_shared.repositories import AuditRepository


class AuditService:
    def __init__(
        self,
        auditRepository: AuditRepository,
    ):
        self.auditRepository = auditRepository

    def listAuditLogs(
        self,
        db: Session,
    ):
        return self.auditRepository.listAll(db)