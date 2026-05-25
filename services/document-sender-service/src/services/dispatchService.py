from datetime import datetime, timezone
from uuid import UUID

from inbox_shared.database import createDbSession
from inbox_shared.enums import (
    AssignmentType,
    AuditAction,
    DepartmentType,
    DocumentLabel,
    DocumentStatus,
)
from inbox_shared.messaging.queueNames import QueueNames
from inbox_shared.repositories import (
    AssignmentRepository,
    AuditRepository,
    DocumentRepository,
    PredictionRepository,
    SystemSettingsRepository,
)
from inbox_shared.services import SettingsService

from src.messaging.rabbitPublisher import publishMessage


class DispatchService:
    def __init__(self) -> None:
        self.documentRepository = DocumentRepository()
        self.predictionRepository = PredictionRepository()
        self.assignmentRepository = AssignmentRepository()
        self.auditRepository = AuditRepository()
        self.settingsService = SettingsService(
            systemSettingsRepository=SystemSettingsRepository(),
        )

    def handleDispatchDocumentRequested(self, channel, event: dict):
        db = createDbSession()

        try:
            documentId = UUID(str(event.get("documentId")))
            targetDepartment = DepartmentType(event.get("targetDepartment"))
            status = DocumentStatus(event.get("status"))
            prediction = event.get("prediction", {})
            correlationId = event.get("correlationId")

            predictedLabel = DocumentLabel(prediction.get("label"))
            confidenceScore = float(prediction.get("confidence"))
            probabilities = prediction.get("probabilities", {})
            modelVersion = prediction.get("modelVersion", "cnn_v1")
            threshold = self.settingsService.getAiThreshold(db)

            document = self.documentRepository.getById(db, documentId)

            if document is None:
                raise RuntimeError(f"Document not found: {documentId}")

            document.predictedLabel = predictedLabel
            document.confidenceScore = confidenceScore
            document.department = targetDepartment
            document.status = status

            if status == DocumentStatus.ROUTED:
                document.finalLabel = predictedLabel

            self.documentRepository.saveDocument(db, document)

            self.predictionRepository.createPrediction(
                db,
                documentId=document.id,
                predictedLabel=predictedLabel,
                confidenceScore=confidenceScore,
                hrProbability=float(probabilities.get("HR", 0)),
                financeProbability=float(probabilities.get("FINANCE", 0)),
                legalProbability=float(probabilities.get("LEGAL", 0)),
                modelVersion=modelVersion,
                thresholdUsed=threshold,
            )

            self.assignmentRepository.createAssignment(
                db,
                documentId=document.id,
                department=targetDepartment,
                assignmentType=AssignmentType.AUTO,
            )

            auditAction = (
                AuditAction.DOCUMENT_ROUTED
                if status == DocumentStatus.ROUTED
                else AuditAction.DOCUMENT_MARKED_REVIEW
            )

            self.auditRepository.create(
                db,
                action=auditAction,
                documentId=document.id,
                details={
                    "targetDepartment": targetDepartment.value,
                    "status": status.value,
                    "predictedLabel": predictedLabel.value,
                    "confidenceScore": confidenceScore,
                    "thresholdUsed": threshold,
                    "correlationId": correlationId,
                },
            )

            completedEvent = {
                "eventType": "DocumentDispatched",
                "documentId": str(document.id),
                "targetDepartment": targetDepartment.value,
                "status": status.value,
                "prediction": prediction,
                "dispatchedAt": datetime.now(timezone.utc).isoformat(),
                "correlationId": correlationId,
            }

            publishMessage(
                channel=channel,
                queueName=QueueNames.senderDocumentCompleted,
                message=completedEvent,
            )

            notificationEvent = {
                "eventType": "NotificationRequested",
                "documentId": str(document.id),
                "targetDepartment": targetDepartment.value,
                "status": status.value,
                "message": f"Document {document.id} dispatched to {targetDepartment.value}",
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "correlationId": correlationId,
            }

            publishMessage(
                channel=channel,
                queueName=QueueNames.notification,
                message=notificationEvent,
            )

            print(
                f"Document {document.id} dispatched successfully. "
                f"targetDepartment={targetDepartment.value}, "
                f"status={status.value}, correlationId={correlationId}"
            )

        finally:
            db.close()