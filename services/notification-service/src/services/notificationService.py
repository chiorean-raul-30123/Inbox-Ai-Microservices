from collections import deque


class NotificationService:
    notifications = deque(maxlen=100)

    def handleNotificationRequested(
        self,
        event: dict,
    ):
        notification = {
            "id": len(self.notifications) + 1,
            "title": event.get(
                "status",
                "Notification",
            ),
            "message": event.get(
                "message",
                "",
            ),
            "targetDepartment": event.get(
                "targetDepartment",
            ),
            "documentId": event.get(
                "documentId",
            ),
            "createdAt": event.get(
                "timestamp",
            ),
        }

        self.notifications.appendleft(
            notification
        )

        print(
            f"Notification stored: {notification}"
        )