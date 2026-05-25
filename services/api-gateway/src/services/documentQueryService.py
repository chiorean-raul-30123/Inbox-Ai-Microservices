import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from inbox_shared.enums import AssignmentType, AuditAction, DepartmentType, DocumentLabel, DocumentStatus
from inbox_shared.exceptions import ResourceNotFoundException
from inbox_shared.models import User
from inbox_shared.repositories import AssignmentRepository, AuditRepository, DocumentRepository
from inbox_shared.services import StorageService
from src.schemas.document import DocumentReviewRequest


class DocumentQueryService:
    def __init__(
        self,
        documentRepository: DocumentRepository,
        assignmentRepository: AssignmentRepository,
        auditRepository: AuditRepository,
        storageService: StorageService,
    ) -> None:
        self.documentRepository = documentRepository
        self.assignmentRepository = assignmentRepository
        self.auditRepository = auditRepository
        self.storageService = storageService

    def getDocument(self, db: Session, documentId: uuid.UUID):
        document = self.documentRepository.getById(db, documentId)

        if document is None:
            raise ResourceNotFoundException("Document not found.")

        return document

    def listDocuments(self, db: Session):
        return self.documentRepository.listAll(db)

    def listDocumentsByDepartment(self, db: Session, department: DepartmentType):
        return self.documentRepository.listByDepartment(db, department)

    def listNeedsReviewDocuments(self, db: Session):
        return self.documentRepository.listByDepartment(
            db,
            DepartmentType.NEEDS_REVIEW,
        )

    def reviewDocument(
        self,
        db: Session,
        *,
        documentId: uuid.UUID,
        request: DocumentReviewRequest,
        currentUser: User,
    ):
        document = self.documentRepository.getById(db, documentId)

        if document is None:
            raise ResourceNotFoundException("Missing document.")

        oldFinalLabel = document.finalLabel.value if document.finalLabel else None
        oldDepartment = document.department.value if document.department else None

        newDepartment = self.mapLabelToDepartment(request.finalLabel)

        document.finalLabel = request.finalLabel
        document.department = newDepartment
        document.status = DocumentStatus.REVIEWED
        document.reviewedBy = currentUser.id
        document.reviewedAt = datetime.now(timezone.utc)

        savedDocument = self.documentRepository.saveDocument(db, document)

        self.assignmentRepository.createAssignment(
            db,
            documentId=document.id,
            department=newDepartment,
            assignmentType=AssignmentType.MANUAL,
            assignedByUserId=currentUser.id,
        )

        self.auditRepository.create(
            db,
            action=AuditAction.DOCUMENT_LABEL_UPDATED,
            userId=currentUser.id,
            documentId=document.id,
            details={
                "oldFinalLabel": oldFinalLabel,
                "newFinalLabel": request.finalLabel.value,
                "oldDepartment": oldDepartment,
                "newDepartment": newDepartment.value,
                "reviewNotes": request.reviewNotes,
            },
        )

        return savedDocument

    def mapLabelToDepartment(self, label: DocumentLabel) -> DepartmentType:
        if label == DocumentLabel.HR:
            return DepartmentType.HR

        if label == DocumentLabel.FINANCE:
            return DepartmentType.FINANCE

        return DepartmentType.LEGAL

    def getDocumentDownloadUrl(
        self,
        db: Session,
        *,
        documentId: uuid.UUID,
    ):
        document = self.documentRepository.getById(db, documentId)

        if document is None:
            raise ResourceNotFoundException("Document not found.")

        downloadUrl = self.storageService.getDownloadUrl(document.filePath)

        return {
            "downloadUrl": downloadUrl,
        }
    
    def moveDocumentToDeleted(
            self,
            db: Session,
            *,
            documentId: uuid.UUID,
            currentUser: User,
        ):
            
            document = self.documentRepository.getById(db, documentId)

            if document is None:
                raise ResourceNotFoundException("Document not found.")

            oldStatus = document.status.value
            document.status = DocumentStatus.DELETED
            document.deletedBy = currentUser.id
            document.deletedAt = datetime.now(timezone.utc)

            savedDocument = self.documentRepository.saveDocument(db, document)

            self.auditRepository.create(
                db,
                action=AuditAction.DOCUMENT_LABEL_UPDATED,
                userId=currentUser.id,
                documentId=document.id,
                details={
                    "oldStatus": oldStatus,
                    "newStatus": DocumentStatus.DELETED.value,
                    "action": "MOVE_TO_DELETED",
                },
            )

            return savedDocument

    def listDeletedDocuments(self, db: Session,currentUser: User):
        return self.documentRepository.listDeletedByUser(
            db,
            currentUser.id,
        )