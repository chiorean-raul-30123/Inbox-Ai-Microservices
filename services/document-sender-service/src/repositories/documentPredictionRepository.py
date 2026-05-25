from sqlalchemy.orm import Session

from inbox_shared.models import DocumentPrediction


class DocumentPredictionRepository:
    def create(self, db: Session, prediction: DocumentPrediction):
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction