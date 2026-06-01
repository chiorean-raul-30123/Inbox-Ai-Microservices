import uuid
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from inbox_shared.database import getDb
from inbox_shared.enums import DepartmentType, RoleType
from inbox_shared.models import User
from inbox_shared.repositories import (
    AssignmentRepository,
    AuditRepository,
    DocumentRepository,
)
from inbox_shared.services import StorageService
from src.api.deps import getCurrentActiveUser, requireRoles
from src.core.config import settings
from src.schemas.document import (
    BulkUploadResponse,
    DocumentDownloadUrlResponse,
    DocumentListItemResponse,
    DocumentResponse,
    DocumentReviewRequest,
)
from src.services.documentQueryService import DocumentQueryService


router = APIRouter(prefix="/documents", tags=["Documents"])


def getDocumentQueryService() -> DocumentQueryService:
    return DocumentQueryService(
        documentRepository=DocumentRepository(),
        assignmentRepository=AssignmentRepository(),
        auditRepository=AuditRepository(),
        storageService=StorageService(),
    )


@router.post("/upload")
async def uploadDocument(
    file: UploadFile = File(...),
    senderEmail: str | None = Form(default=None),
    senderName: str | None = Form(default=None),
    subject: str | None = Form(default=None),
    body: str | None = Form(default=None),
):
    data = {}

    if senderEmail:
        data["senderEmail"] = senderEmail

    if senderName:
        data["senderName"] = senderName

    if subject:
        data["subject"] = subject

    if body:
        data["body"] = body

    async with httpx.AsyncClient(timeout=60.0) as client:
        files = {
            "file": (
                file.filename,
                await file.read(),
                file.content_type,
            )
        }

        response = await client.post(
            f"{settings.uploadInputServiceUrl}/upload",
            data=data,
            files=files,
        )

    if response.status_code >= 400:
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )

    return response.json()


@router.post("/upload-bulk", response_model=BulkUploadResponse)
async def uploadBulkDocuments(
    files: Annotated[list[UploadFile], File(description="PDF files to upload")],
):
    multipartFiles = []

    for file in files:
        multipartFiles.append(
            (
                "files",
                (
                    file.filename,
                    await file.read(),
                    file.content_type,
                ),
            )
        )

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.uploadInputServiceUrl}/upload/bulk",
            files=multipartFiles,
        )

    if response.status_code >= 400:
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )

    return response.json()


@router.get(
    "",
    response_model=list[DocumentListItemResponse],
    response_model_by_alias=True,
)
def listDocuments(
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN)),
    documentService: DocumentQueryService = Depends(getDocumentQueryService),
):
    documents = documentService.listDocuments(db)
    return [DocumentListItemResponse.model_validate(document) for document in documents]


@router.get(
    "/inbox/hr",
    response_model=list[DocumentListItemResponse],
    response_model_by_alias=True,
)
def getHrInbox(
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN, RoleType.HR)),
    documentService: DocumentQueryService = Depends(getDocumentQueryService),
):
    documents = documentService.listDocumentsByDepartment(db, DepartmentType.HR)
    return [DocumentListItemResponse.model_validate(document) for document in documents]


@router.get(
    "/inbox/finance",
    response_model=list[DocumentListItemResponse],
    response_model_by_alias=True,
)
def getFinanceInbox(
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN, RoleType.FINANCE)),
    documentService: DocumentQueryService = Depends(getDocumentQueryService),
):
    documents = documentService.listDocumentsByDepartment(db, DepartmentType.FINANCE)
    return [DocumentListItemResponse.model_validate(document) for document in documents]


@router.get(
    "/inbox/legal",
    response_model=list[DocumentListItemResponse],
    response_model_by_alias=True,
)
def getLegalInbox(
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN, RoleType.LEGAL)),
    documentService: DocumentQueryService = Depends(getDocumentQueryService),
):
    documents = documentService.listDocumentsByDepartment(db, DepartmentType.LEGAL)
    return [DocumentListItemResponse.model_validate(document) for document in documents]


@router.get(
    "/inbox/needs-review",
    response_model=list[DocumentListItemResponse],
    response_model_by_alias=True,
)
def getNeedsReviewInbox(
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN)),
    documentService: DocumentQueryService = Depends(getDocumentQueryService),
):
    documents = documentService.listDocumentsByDepartment(
        db,
        DepartmentType.NEEDS_REVIEW,
    )
    return [DocumentListItemResponse.model_validate(document) for document in documents]


@router.get(
    "/deleted",
    response_model=list[DocumentListItemResponse],
    response_model_by_alias=True,
)
def getDeletedDocuments(
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentActiveUser),
    documentService: DocumentQueryService = Depends(getDocumentQueryService),
):
    documents = documentService.listDeletedDocuments(
        db,
        currentUser=currentUser,
    )

    return [DocumentListItemResponse.model_validate(document) for document in documents]


@router.get("/{documentId}/download-url", response_model=DocumentDownloadUrlResponse)
def getDocumentDownloadUrl(
    documentId: uuid.UUID,
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentActiveUser),
    documentService: DocumentQueryService = Depends(getDocumentQueryService),
):
    return documentService.getDocumentDownloadUrl(
        db,
        documentId=documentId,
        currentUser=currentUser,
    )


@router.post(
    "/{documentId}/review",
    response_model=DocumentResponse,
    response_model_by_alias=True,
)
def reviewDocument(
    documentId: uuid.UUID,
    request: DocumentReviewRequest,
    db: Session = Depends(getDb),
    currentUser: User = Depends(
        requireRoles(RoleType.ADMIN)
    ),
    documentService: DocumentQueryService = Depends(getDocumentQueryService),
):
    document = documentService.reviewDocument(
        db,
        documentId=documentId,
        request=request,
        currentUser=currentUser,
    )

    return DocumentResponse.model_validate(document)


@router.post(
    "/{documentId}/delete",
    response_model=DocumentResponse,
    response_model_by_alias=True,
)
def moveDocumentToDeleted(
    documentId: uuid.UUID,
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentActiveUser),
    documentService: DocumentQueryService = Depends(getDocumentQueryService),
):
    document = documentService.moveDocumentToDeleted(
        db,
        documentId=documentId,
        currentUser=currentUser,
    )

    return DocumentResponse.model_validate(document)


@router.get(
    "/{documentId}",
    response_model=DocumentResponse,
    response_model_by_alias=True,
)
def getDocument(
    documentId: uuid.UUID,
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentActiveUser),
    documentService: DocumentQueryService = Depends(getDocumentQueryService),
):
    document = documentService.getDocument(
        db,
        documentId=documentId,
        currentUser=currentUser,
    )

    return DocumentResponse.model_validate(document)