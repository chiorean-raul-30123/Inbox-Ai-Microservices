from src.messaging.inputConsumer import createInputCallback
from src.messaging.processorResultConsumer import createProcessorResultCallback
from inbox_shared.messaging.queueNames import QueueNames
from src.messaging.queueSetup import declareQueues
from src.messaging.rabbitConnection import createRabbitConnection
from src.messaging.failedEventConsumer import createFailedEventCallback


def main():
    connection = createRabbitConnection()
    channel = connection.channel()

    declareQueues(channel)

    channel.basic_qos(prefetch_count=1)

    inputCallback = createInputCallback(channel)
    processorResultCallback = createProcessorResultCallback(channel)
    failedEventCallback = createFailedEventCallback(channel)

    inputQueues = [
        QueueNames.inputUploadReceived,
        QueueNames.inputEmailReceived,
        QueueNames.inputScanReceived,
    ]

    for queueName in inputQueues:
        channel.basic_consume(
            queue=queueName,
            on_message_callback=inputCallback,
        )

    processorResultQueues = [
        QueueNames.processorDocumentCompleted,
    ]

    for queueName in processorResultQueues:
        channel.basic_consume(
            queue=queueName,
            on_message_callback=processorResultCallback,
        )

    failedQueues = [
        QueueNames.processorDocumentFailed,
        QueueNames.senderDocumentFailed,
    ]

    for queueName in failedQueues:
        channel.basic_consume(
            queue=queueName,
            on_message_callback=failedEventCallback,
        )
    
    print("Document Orchestrator Service started.")
    print("Listening for input document events and processor results...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping Document Orchestrator Service...")
        channel.stop_consuming()
        connection.close()


if __name__ == "__main__":
    main()