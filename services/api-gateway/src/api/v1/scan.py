from typing import Annotated

import httpx
from fastapi import APIRouter, File, Form, UploadFile

from src.core.config import settings


router = APIRouter(prefix="/scan", tags=["Scan"])


@router.post("/upload")
async def uploadScan(
    file: Annotated[UploadFile, File(...)],
    submittedBy: Annotated[str | None, Form()] = None,
):
    data = {}

    if submittedBy is not None:
        data["submittedBy"] = submittedBy

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

    response.raise_for_status()
    return response.json()