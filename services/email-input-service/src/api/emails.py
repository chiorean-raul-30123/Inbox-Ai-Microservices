from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from src.services.emailInputService import EmailInputService


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