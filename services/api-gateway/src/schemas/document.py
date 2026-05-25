from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from inbox_shared.enums import AssignmentType, DepartmentType, DocumentLabel, DocumentStatus
from src.schemas.user import UserSummaryResponse


class DocumentPredictionResponse(BaseModel):
    id: UUID
    predictedLabel: DocumentLabel = Field(serialization_alias="predicted_label")
    confidenceScore: float = Field(serialization_alias="confidence_score")
    hrProbability: float = Field(serialization_alias="hr_probability")
    financeProbability: float = Field(serialization_alias="finance_probability")
    legalProbability: float = Field(serialization_alias="legal_probability")
    modelVersion: str = Field(serialization_alias="model_version")
    thresholdUsed: float = Field(serialization_alias="threshold_used")
    createdAt: datetime = Field(serialization_alias="created_at")
    updatedAt: datetime = Field(serialization_alias="updated_at")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class DocumentAssignmentResponse(BaseModel):
    id: UUID
    department: DepartmentType
    assignmentType: AssignmentType = Field(serialization_alias="assignment_type")
    assignedToUser: UserSummaryResponse | None = Field(
        default=None,
        serialization_alias="assigned_to_user",
    )
    assignedByUser: UserSummaryResponse | None = Field(
        default=None,
        serialization_alias="assigned_by_user",
    )
    createdAt: datetime = Field(serialization_alias="created_at")
    updatedAt: datetime = Field(serialization_alias="updated_at")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class DocumentListItemResponse(BaseModel):
    id: UUID
    originalFilename: str = Field(serialization_alias="original_filename")
    mimeType: str = Field(serialization_alias="mime_type")
    fileSize: int = Field(serialization_alias="file_size")
    status: DocumentStatus
    predictedLabel: DocumentLabel | None = Field(
        default=None,
        serialization_alias="predicted_label",
    )
    finalLabel: DocumentLabel | None = Field(
        default=None,
        serialization_alias="final_label",
    )
    department: DepartmentType | None = None
    confidenceScore: float | None = Field(
        default=None,
        serialization_alias="confidence_score",
    )
    createdAt: datetime = Field(serialization_alias="created_at")
    updatedAt: datetime = Field(serialization_alias="updated_at")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class DocumentResponse(BaseModel):
    id: UUID
    originalFilename: str = Field(serialization_alias="original_filename")
    storedFilename: str = Field(serialization_alias="stored_filename")
    filePath: str = Field(serialization_alias="file_path")
    mimeType: str = Field(serialization_alias="mime_type")
    fileSize: int = Field(serialization_alias="file_size")

    status: DocumentStatus
    predictedLabel: DocumentLabel | None = Field(
        default=None,
        serialization_alias="predicted_label",
    )
    finalLabel: DocumentLabel | None = Field(
        default=None,
        serialization_alias="final_label",
    )
    department: DepartmentType | None = None
    confidenceScore: float | None = Field(
        default=None,
        serialization_alias="confidence_score",
    )

    reviewedAt: datetime | None = Field(
        default=None,
        serialization_alias="reviewed_at",
    )

    uploader: UserSummaryResponse | None = None
    reviewer: UserSummaryResponse | None = None

    predictions: list[DocumentPredictionResponse] = []
    assignments: list[DocumentAssignmentResponse] = []

    createdAt: datetime = Field(serialization_alias="created_at")
    updatedAt: datetime = Field(serialization_alias="updated_at")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class DocumentUploadResponse(BaseModel):
    id: UUID
    originalFilename: str = Field(serialization_alias="original_filename")
    status: DocumentStatus
    message: str

    model_config = ConfigDict(populate_by_name=True)


class DocumentReviewRequest(BaseModel):
    finalLabel: DocumentLabel
    reviewNotes: str | None = Field(default=None, max_length=1000)


class BulkUploadItemResponse(BaseModel):
    originalFilename: str
    documentId: UUID | None = None
    status: DocumentStatus | None = None
    department: DepartmentType | None = None
    success: bool
    message: str


class BulkUploadResponse(BaseModel):
    uploadedDocuments: list[BulkUploadItemResponse]
    failedDocuments: list[BulkUploadItemResponse]


class DocumentDownloadUrlResponse(BaseModel):
    downloadUrl: str