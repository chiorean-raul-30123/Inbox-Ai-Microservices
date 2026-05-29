from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from src.services.uploadService import UploadService
from fastapi import Form


router = APIRouter(prefix="/upload", tags=["Upload"])


def getUploadService() -> UploadService:
    return UploadService()


@router.post("")
def uploadDocument(
    file: Annotated[UploadFile, File(...)],
    senderEmail: Annotated[str | None, Form()] = None,
    senderName: Annotated[str | None, Form()] = None,
    subject: Annotated[str | None, Form()] = None,
    body: Annotated[str | None, Form()] = None,
):
    uploadService = getUploadService()

    return uploadService.uploadDocument(
        file=file,
        uploadedBy=None,
        senderEmail=senderEmail,
        senderName=senderName,
        subject=subject,
        body=body,
    )


@router.post("/bulk")
def uploadBulkDocuments(
    files: Annotated[list[UploadFile], File(...)],
):
    uploadService = getUploadService()

    uploadedDocuments = []
    failedDocuments = []

    for file in files:
        try:
            uploadedDocuments.append(
                uploadService.uploadDocument(
                    file=file,
                    uploadedBy=None,
                )
            )
        except Exception as exception:
            failedDocuments.append(
                {
                    "originalFilename": file.filename or "unknown",
                    "success": False,
                    "message": str(exception),
                }
            )

    return {
        "uploadedDocuments": uploadedDocuments,
        "failedDocuments": failedDocuments,
    }