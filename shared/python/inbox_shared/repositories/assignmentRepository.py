import uuid

from sqlalchemy.orm import Session

from inbox_shared.enums import AssignmentType, DepartmentType
from inbox_shared.models import DocumentAssignment


class AssignmentRepository:
    def createAssignment(
        self,
        db: Session,
        *,
        documentId: uuid.UUID,
        department: DepartmentType,
        assignmentType: AssignmentType,
        assignedToUserId: uuid.UUID | None = None,
        assignedByUserId: uuid.UUID | None = None,
    ) -> DocumentAssignment:
        assignment = DocumentAssignment(
            documentId=documentId,
            department=department,
            assignmentType=assignmentType,
            assignedToUserId=assignedToUserId,
            assignedByUserId=assignedByUserId,
        )

        db.add(assignment)
        db.commit()
        db.refresh(assignment)

        return assignment