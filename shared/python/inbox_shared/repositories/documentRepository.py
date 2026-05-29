import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from inbox_shared.enums import DepartmentType, DocumentStatus
from inbox_shared.models import Document


class DocumentRepository:
    def create(
        self,
        db: Session,
        *,
        originalFilename: str,
        storedFilename: str,
        filePath: str,
        mimeType: str,
        fileSize: int,
        uploadedBy: uuid.UUID | None,
        status: DocumentStatus = DocumentStatus.RECEIVED,
    ) -> Document:
        document = Document(
            originalFilename=originalFilename,
            storedFilename=storedFilename,
            filePath=filePath,
            mimeType=mimeType,
            fileSize=fileSize,
            uploadedBy=uploadedBy,
            status=status,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    def getById(self, db: Session, documentId: uuid.UUID) -> Document | None:
        stmt = (
            select(Document)
            .options(
                joinedload(Document.uploader),
                joinedload(Document.reviewer),
                joinedload(Document.predictions),
                joinedload(Document.assignments),
                joinedload(Document.incomingEmail),
            )
            .where(Document.id == documentId)
        )

        return db.execute(stmt).unique().scalar_one_or_none()

    def listAll(self, db: Session) -> list[Document]:
        stmt = (
            select(Document)
            .options(
                joinedload(Document.uploader),
                joinedload(Document.reviewer),
                joinedload(Document.incomingEmail),
            )
            .order_by(Document.createdAt.desc())
        )

        return list(db.execute(stmt).unique().scalars().all())

    def listByStatus(self, db: Session, status: DocumentStatus) -> list[Document]:
        stmt = (
            select(Document)
            .options(
                joinedload(Document.uploader),
                joinedload(Document.reviewer),
                joinedload(Document.incomingEmail),
            )
            .where(Document.status == status)
            .order_by(Document.createdAt.desc())
        )

        return list(db.execute(stmt).unique().scalars().all())

    def listByDepartment(
        self,
        db: Session,
        department: DepartmentType,
    ) -> list[Document]:
        stmt = (
            select(Document)
            .options(
                joinedload(Document.uploader),
                joinedload(Document.reviewer),
                joinedload(Document.incomingEmail),
            )
            .where(Document.department == department)
            .where(Document.status != DocumentStatus.DELETED)
            .order_by(Document.createdAt.desc())
        )

        return list(db.execute(stmt).unique().scalars().all())

    def saveDocument(self, db: Session, document: Document) -> Document:
        db.add(document)
        db.commit()
        db.refresh(document)

        return document
    

    def listDeletedByUser(self, db: Session, userId: uuid.UUID) -> list[Document]:
        stmt = (
            select(Document)
            .options(
                joinedload(Document.uploader),
                joinedload(Document.reviewer),
                joinedload(Document.incomingEmail),
            )
            .where(Document.status == DocumentStatus.DELETED)
            .where(Document.deletedBy == userId)
            .order_by(Document.deletedAt.desc())
        )

        return list(db.execute(stmt).unique().scalars().all())