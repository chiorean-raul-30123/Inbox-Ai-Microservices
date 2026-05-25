from sqlalchemy.orm import Session

from inbox_shared.models import AuditLog


class AuditLogRepository:
    def create(self, db: Session, auditLog: AuditLog):
        db.add(auditLog)
        db.commit()
        db.refresh(auditLog)
        return auditLog