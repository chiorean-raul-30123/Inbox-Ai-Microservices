from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from src.services.scanInputService import ScanInputService


router = APIRouter(prefix="/scan", tags=["Scan"])


def getScanInputService() -> ScanInputService:
    return ScanInputService()


@router.post("/upload")
def uploadScan(
    file: Annotated[UploadFile, File(...)],
    submittedBy: Annotated[str | None, Form()] = None,
    senderEmail: Annotated[str | None, Form()] = None,
    senderName: Annotated[str | None, Form()] = None,
    subject: Annotated[str | None, Form()] = None,
    body: Annotated[str | None, Form()] = None,
):
    scanInputService = getScanInputService()

    return scanInputService.uploadScan(
        file=file,
        submittedBy=submittedBy,
        senderEmail=senderEmail,
        senderName=senderName,
        subject=subject,
        body=body,
    )