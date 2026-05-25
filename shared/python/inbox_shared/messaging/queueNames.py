class QueueNames:
    inputUploadReceived = "input.upload.received.queue"
    inputEmailReceived = "input.email.received.queue"
    inputScanReceived = "input.scan.received.queue"

    processorDocumentRequested = "processor.document.requested.queue"
    processorDocumentCompleted = "processor.document.completed.queue"
    processorDocumentFailed = "processor.document.failed.queue"

    senderDocumentDispatch = "sender.document.dispatch.queue"
    senderDocumentCompleted = "sender.document.completed.queue"
    senderDocumentFailed = "sender.document.failed.queue"

    notification = "notification.queue"
    deadLetter = "deadLetter.queue"