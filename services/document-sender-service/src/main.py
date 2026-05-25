from inbox_shared.messaging.queueNames import QueueNames
from src.messaging.rabbitConnection import createRabbitConnection
from src.messaging.senderConsumer import createSenderCallback


def main():
    connection = createRabbitConnection()
    channel = connection.channel()

    queueNames = [
        QueueNames.senderDocumentDispatch,
        QueueNames.senderDocumentCompleted,
        QueueNames.senderDocumentFailed,
        QueueNames.notification,
    ]

    for queueName in queueNames:
        channel.queue_declare(queue=queueName, durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QueueNames.senderDocumentDispatch,
        on_message_callback=createSenderCallback(channel),
    )

    print("Document Sender Service started.")
    print("Listening for document dispatch requests...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping Document Sender Service...")
        channel.stop_consuming()
        connection.close()


if __name__ == "__main__":
    main()