from typing import Annotated

import httpx
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from src.core.config import settings


router = APIRouter(prefix="/scan", tags=["Scan"])


@router.post("/upload")
async def uploadScan(
    file: Annotated[UploadFile, File(...)],
    submittedBy: Annotated[str | None, Form()] = None,
    senderEmail: Annotated[str | None, Form()] = None,
    senderName: Annotated[str | None, Form()] = None,
    subject: Annotated[str | None, Form()] = None,
    body: Annotated[str | None, Form()] = None,
):
    data = {}

    for key, value in {
        "submittedBy": submittedBy,
        "senderEmail": senderEmail,
        "senderName": senderName,
        "subject": subject,
        "body": body,
    }.items():
        if value is not None:
            data[key] = value

    files = {
        "file": (
            file.filename,
            await file.read(),
            file.content_type,
        )
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.scanInputServiceUrl}/scan/upload",
            data=data,
            files=files,
        )

    if response.status_code >= 400:
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )

    return response.json()