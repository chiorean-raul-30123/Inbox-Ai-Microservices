from src.messaging.processorConsumer import createProcessorCallback
from inbox_shared.messaging.queueNames import QueueNames
from src.messaging.rabbitConnection import createRabbitConnection


def main():
    connection = createRabbitConnection()
    channel = connection.channel()

    channel.queue_declare(
        queue=QueueNames.processorDocumentRequested,
        durable=True,
    )
    channel.queue_declare(
        queue=QueueNames.processorDocumentCompleted,
        durable=True,
    )
    channel.queue_declare(
        queue=QueueNames.processorDocumentFailed,
        durable=True,
    )

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QueueNames.processorDocumentRequested,
        on_message_callback=createProcessorCallback(channel),
    )

    print("Document Processor Service started.")
    print("Listening for processor document requests...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping Document Processor Service...")
        channel.stop_consuming()
        connection.close()


if __name__ == "__main__":
    main()