import uuid

from inbox_shared.database import createDbSession
from inbox_shared.repositories import NotificationRepository


class NotificationService:
    def __init__(self) -> None:
        self.notificationRepository = NotificationRepository()

    def handleNotificationRequested(self, event: dict):
        documentIdValue = event.get("documentId")

        documentId = None
        if documentIdValue:
            try:
                documentId = uuid.UUID(str(documentIdValue))
            except ValueError:
                documentId = None

        targetDepartment = event.get("targetDepartment")
        status = event.get("status")
        message = event.get("message") or "A document event was processed."
        correlationId = event.get("correlationId")

        title = self.buildTitle(
            status=status,
            targetDepartment=targetDepartment,
        )

        db = createDbSession()

        try:
            notification = self.notificationRepository.create(
                db,
                title=title,
                message=message,
                status=status,
                targetDepartment=targetDepartment,
                documentId=documentId,
                correlationId=correlationId,
            )

            print("Notification stored:")
            print(f"id={notification.id}")
            print(f"title={notification.title}")
            print(f"documentId={documentId}")
            print(f"targetDepartment={targetDepartment}")
            print(f"status={status}")
            print(f"correlationId={correlationId}")

        finally:
            db.close()

    def buildTitle(
        self,
        *,
        status: str | None,
        targetDepartment: str | None,
    ) -> str:
        if status == "ROUTED" and targetDepartment:
            return f"Document routed to {targetDepartment}"

        if status == "NEEDS_REVIEW":
            return "Document requires review"

        if status and "FAILED" in status:
            return "Document processing failed"

        return "Document notification"