import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from inbox_shared.database import getDb
from inbox_shared.models import User
from inbox_shared.repositories import NotificationRepository

from src.api.deps import getCurrentActiveUser
from src.schemas.notification import NotificationListResponse, NotificationResponse
from src.services.notificationService import NotificationQueryService


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


def getNotificationService() -> NotificationQueryService:
    return NotificationQueryService(
        notificationRepository=NotificationRepository(),
    )


@router.get("", response_model=NotificationListResponse, response_model_by_alias=True)
def getNotifications(
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentActiveUser),
    notificationService: NotificationQueryService = Depends(getNotificationService),
):
    notifications, unreadCount = notificationService.listNotifications(db)

    return NotificationListResponse(
        notifications=[
            NotificationResponse.model_validate(notification)
            for notification in notifications
        ],
        unreadCount=unreadCount,
    )


@router.patch(
    "/{notificationId}/read",
    response_model=NotificationResponse,
    response_model_by_alias=True,
)
def markNotificationAsRead(
    notificationId: uuid.UUID,
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentActiveUser),
    notificationService: NotificationQueryService = Depends(getNotificationService),
):
    notification = notificationService.markAsRead(
        db,
        notificationId=notificationId,
    )

    return NotificationResponse.model_validate(notification)


@router.patch("/read-all")
def markAllNotificationsAsRead(
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentActiveUser),
    notificationService: NotificationQueryService = Depends(getNotificationService),
):
    notificationService.markAllAsRead(db)

    return {"message": "All notifications marked as read."}