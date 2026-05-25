import json

from src.services.notificationService import NotificationService


notificationService = NotificationService()


def createNotificationCallback():
    def callback(ch, method, properties, body):
        try:
            event = json.loads(body.decode("utf-8"))

            notificationService.handleNotificationRequested(event)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as exception:
            print(f"Failed to handle notification: {exception}")
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False,
            )

    return callback