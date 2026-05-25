from sqlalchemy.orm import Session

from inbox_shared.models import DocumentAssignment


class DocumentAssignmentRepository:
    def create(self, db: Session, assignment: DocumentAssignment):
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment