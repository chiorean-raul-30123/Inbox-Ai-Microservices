import uuid

from sqlalchemy.orm import Session

from inbox_shared.exceptions import ResourceNotFoundException
from inbox_shared.repositories import NotificationRepository


class NotificationQueryService:
    def __init__(
        self,
        notificationRepository: NotificationRepository,
    ) -> None:
        self.notificationRepository = notificationRepository

    def listNotifications(self, db: Session):
        notifications = self.notificationRepository.listLatest(db)
        unreadCount = self.notificationRepository.countUnread(db)

        return notifications, unreadCount

    def markAsRead(
        self,
        db: Session,
        notificationId: uuid.UUID,
    ):
        notification = self.notificationRepository.getById(db, notificationId)

        if notification is None:
            raise ResourceNotFoundException("Notification not found.")

        notification.isRead = True

        return self.notificationRepository.save(db, notification)

    def markAllAsRead(self, db: Session) -> None:
        self.notificationRepository.markAllAsRead(db)