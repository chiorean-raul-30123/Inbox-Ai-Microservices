import uuid
from typing import Any

from sqlalchemy.orm import Session

from inbox_shared.enums import AuditAction
from inbox_shared.models import AuditLog
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class AuditRepository:
    def create(
        self,
        db: Session,
        *,
        action: AuditAction,
        userId: uuid.UUID | None = None,
        documentId: uuid.UUID | None = None,
        details: dict[str, Any] | None = None,
    ) -> AuditLog:
        auditLog = AuditLog(
            action=action,
            userId=userId,
            documentId=documentId,
            details=details,
        )

        db.add(auditLog)
        db.commit()
        db.refresh(auditLog)

        return auditLog
    
    def listAll(
        self,
        db: Session,
    ) -> list[AuditLog]:
        stmt = (
            select(AuditLog)
            .options(
                joinedload(AuditLog.user),
                joinedload(AuditLog.document),
            )
            .order_by(
                AuditLog.createdAt.desc()
            )
        )

        return list(
            db.execute(stmt)
            .unique()
            .scalars()
            .all()
        )