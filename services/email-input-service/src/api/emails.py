from typing import Annotated
from fastapi import APIRouter, File, Form, UploadFile, Request
from src.services.emailInputService import EmailInputService
from src.schemas.mailpitWebhook import MailpitWebhookRequest


router = APIRouter(prefix="/emails", tags=["Emails"])


def getEmailInputService() -> EmailInputService:
    return EmailInputService()


@router.post("/simulate")
def simulateIncomingEmail(
    senderEmail: Annotated[str, Form()],
    subject: Annotated[str, Form()],
    attachments: Annotated[list[UploadFile], File(...)],
    senderName: Annotated[str | None, Form()] = None,
    body: Annotated[str | None, Form()] = None,
):
    emailInputService = getEmailInputService()

    return emailInputService.processSimulatedEmail(
        senderEmail=senderEmail,
        senderName=senderName,
        subject=subject,
        body=body,
        attachments=attachments,
    )

@router.post("/mailpit/webhook")
async def receiveMailpitWebhook(request: Request):
    payload = await request.json()

    print("MAILPIT WEBHOOK HIT")
    print("MAILPIT WEBHOOK PAYLOAD:", payload)

    webhookRequest = MailpitWebhookRequest.model_validate(payload)
    messageId = webhookRequest.getMessageId()

    emailInputService = getEmailInputService()

    return emailInputService.processMailpitWebhook(
        messageId=messageId,
    )