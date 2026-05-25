import uuid

from sqlalchemy.orm import Session

from inbox_shared.enums import DocumentLabel
from inbox_shared.models import DocumentPrediction


class PredictionRepository:
    def createPrediction(
        self,
        db: Session,
        *,
        documentId: uuid.UUID,
        predictedLabel: DocumentLabel,
        confidenceScore: float,
        hrProbability: float,
        financeProbability: float,
        legalProbability: float,
        modelVersion: str,
        thresholdUsed: float,
    ) -> DocumentPrediction:
        prediction = DocumentPrediction(
            documentId=documentId,
            predictedLabel=predictedLabel,
            confidenceScore=confidenceScore,
            hrProbability=hrProbability,
            financeProbability=financeProbability,
            legalProbability=legalProbability,
            modelVersion=modelVersion,
            thresholdUsed=thresholdUsed,
        )

        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        return prediction