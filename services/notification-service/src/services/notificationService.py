class NotificationService:
    def handleNotificationRequested(self, event: dict):
        documentId = event.get("documentId")
        targetDepartment = event.get("targetDepartment")
        status = event.get("status")
        message = event.get("message")
        correlationId = event.get("correlationId")

        print("Notification received:")
        print(f"documentId={documentId}")
        print(f"targetDepartment={targetDepartment}")
        print(f"status={status}")
        print(f"message={message}")
        print(f"correlationId={correlationId}")