from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from src.services.uploadService import UploadService


router = APIRouter(prefix="/upload", tags=["Upload"])


def getUploadService() -> UploadService:
    return UploadService()


@router.post("")
def uploadDocument(
    file: Annotated[UploadFile, File(...)],
):
    uploadService = getUploadService()

    return uploadService.uploadDocument(
        file=file,
        uploadedBy=None,
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