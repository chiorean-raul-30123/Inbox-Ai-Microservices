from sqlalchemy import select
from sqlalchemy.orm import Session

from inbox_shared.models import Document


class DocumentRepository:
    def getById(self, db: Session, documentId):
        stmt = select(Document).where(Document.id == documentId)
        return db.execute(stmt).scalar_one_or_none()

    def save(self, db: Session, document: Document):
        db.add(document)
        db.commit()
        db.refresh(document)
        return document