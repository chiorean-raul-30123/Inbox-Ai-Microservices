from inbox_shared.messaging.queueNames import QueueNames


def declareQueues(channel):
    queueNames = [
        QueueNames.inputUploadReceived,
        QueueNames.inputEmailReceived,
        QueueNames.inputScanReceived,
        QueueNames.processorDocumentRequested,
        QueueNames.processorDocumentCompleted,
        QueueNames.processorDocumentFailed,
        QueueNames.senderDocumentDispatch,
        QueueNames.senderDocumentCompleted,
        QueueNames.senderDocumentFailed,
        QueueNames.notification,
        QueueNames.deadLetter,
    ]

    for queueName in queueNames:
        channel.queue_declare(queue=queueName, durable=True)