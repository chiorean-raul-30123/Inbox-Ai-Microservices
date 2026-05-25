import uuid

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inbox_shared.database import Base
from inbox_shared.enums import DocumentLabel
from inbox_shared.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class DocumentPrediction(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "document_predictions"

    documentId: Mapped[uuid.UUID] = mapped_column(
        "document_id",
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    predictedLabel: Mapped[DocumentLabel] = mapped_column(
        "predicted_label",
        SqlEnum(DocumentLabel, name="prediction_label_enum"),
        nullable=False,
    )

    confidenceScore: Mapped[float] = mapped_column(
        "confidence_score",
        Numeric(5, 4),
        nullable=False,
    )

    hrProbability: Mapped[float] = mapped_column(
        "hr_probability",
        Numeric(5, 4),
        nullable=False,
    )

    financeProbability: Mapped[float] = mapped_column(
        "finance_probability",
        Numeric(5, 4),
        nullable=False,
    )

    legalProbability: Mapped[float] = mapped_column(
        "legal_probability",
        Numeric(5, 4),
        nullable=False,
    )

    modelVersion: Mapped[str] = mapped_column(
        "model_version",
        String(100),
        nullable=False,
    )

    thresholdUsed: Mapped[float] = mapped_column(
        "threshold_used",
        Numeric(5, 4),
        nullable=False,
    )

    document = relationship(
        "Document",
        back_populates="predictions",
    )