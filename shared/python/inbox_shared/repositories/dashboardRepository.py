from sqlalchemy import func, select
from sqlalchemy.orm import Session

from inbox_shared.enums import DepartmentType, DocumentStatus
from inbox_shared.models import Document


class DashboardRepository:
    def countAllDocuments(self, db: Session) -> int:
        stmt = select(func.count(Document.id))
        return db.execute(stmt).scalar() or 0

    def countDocumentsByStatus(self, db: Session, status: DocumentStatus) -> int:
        stmt = select(func.count(Document.id)).where(Document.status == status)
        return db.execute(stmt).scalar() or 0

    def countDocumentsByDepartment(self, db: Session, department: DepartmentType) -> int:
        stmt = select(func.count(Document.id)).where(Document.department == department)
        return db.execute(stmt).scalar() or 0

    def getAverageConfidence(self, db: Session) -> float | None:
        stmt = select(func.avg(Document.confidenceScore))
        value = db.execute(stmt).scalar()

        if value is None:
            return None

        return float(value)