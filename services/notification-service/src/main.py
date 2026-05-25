from src.messaging.notificationConsumer import createNotificationCallback
from inbox_shared.messaging.queueNames import QueueNames
from src.messaging.rabbitConnection import createRabbitConnection


def main():
    connection = createRabbitConnection()
    channel = connection.channel()

    channel.queue_declare(
        queue=QueueNames.notification,
        durable=True,
    )

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QueueNames.notification,
        on_message_callback=createNotificationCallback(),
    )

    print("Notification Service started.")
    print("Listening for notification events...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping Notification Service...")
        channel.stop_consuming()
        connection.close()


if __name__ == "__main__":
    main()