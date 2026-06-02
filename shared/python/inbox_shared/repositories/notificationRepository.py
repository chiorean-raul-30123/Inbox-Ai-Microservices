import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from inbox_shared.models import Notification


class NotificationRepository:
    def create(
        self,
        db: Session,
        *,
        title: str,
        message: str,
        status: str | None = None,
        targetDepartment: str | None = None,
        documentId: uuid.UUID | None = None,
        correlationId: str | None = None,
    ) -> Notification:
        notification = Notification(
            title=title,
            message=message,
            status=status,
            targetDepartment=targetDepartment,
            documentId=documentId,
            correlationId=correlationId,
            isRead=False,
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification

    def listLatest(
        self,
        db: Session,
        limit: int = 50,
    ) -> list[Notification]:
        stmt = (
            select(Notification)
            .order_by(Notification.createdAt.desc())
            .limit(limit)
        )

        return list(db.execute(stmt).scalars().all())

    def countUnread(self, db: Session) -> int:
        stmt = select(Notification).where(Notification.isRead == False)

        return len(list(db.execute(stmt).scalars().all()))

    def getById(
        self,
        db: Session,
        notificationId: uuid.UUID,
    ) -> Notification | None:
        stmt = select(Notification).where(Notification.id == notificationId)

        return db.execute(stmt).scalar_one_or_none()

    def save(
        self,
        db: Session,
        notification: Notification,
    ) -> Notification:
        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification

    def markAllAsRead(self, db: Session) -> None:
        notifications = db.execute(
            select(Notification).where(Notification.isRead == False)
        ).scalars().all()

        for notification in notifications:
            notification.isRead = True
            db.add(notification)

        db.commit()