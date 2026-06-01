from typing import Annotated
from fastapi.responses import JSONResponse

import httpx
from fastapi import APIRouter, Depends, File, Form, UploadFile

from inbox_shared.enums import RoleType
from inbox_shared.models import User
from src.api.deps import requireRoles
from src.core.config import settings


router = APIRouter(prefix="/emails", tags=["Emails"])


@router.post("/simulate")
async def simulateIncomingEmail(
    senderEmail: Annotated[str, Form()],
    subject: Annotated[str, Form()],
    attachments: Annotated[list[UploadFile], File(...)],
    senderName: Annotated[str | None, Form()] = None,
    body: Annotated[str | None, Form()] = None,
    currentUser: User = Depends(requireRoles(RoleType.ADMIN)),
):
    multipartFiles = []

    for attachment in attachments:
        multipartFiles.append(
            (
                "attachments",
                (
                    attachment.filename,
                    await attachment.read(),
                    attachment.content_type,
                ),
            )
        )

    data = {
        "senderEmail": senderEmail,
        "subject": subject,
    }

    if senderName is not None:
        data["senderName"] = senderName

    if body is not None:
        data["body"] = body

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.emailInputServiceUrl}/emails/simulate",
            data=data,
            files=multipartFiles,
        )

    if response.status_code >= 400:
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )

    return response.json()