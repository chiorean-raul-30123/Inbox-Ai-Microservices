from fastapi import FastAPI,Request

from src.api.upload import router as uploadRouter
from fastapi.responses import JSONResponse

from inbox_shared.exceptions import (
    AppException,
    AuthenticationException,
    AuthorizationException,
    ConflictException,
    ResourceNotFoundException,
    ValidationException,
    SecurityScanException,
)


app = FastAPI(
    title="Inbox AI Upload Input Service",
    version="1.0.0",
)

app.include_router(uploadRouter)

@app.exception_handler(ValidationException)
async def validationExceptionHandler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=400,
        content={
            "errorType": exc.__class__.__name__,
            "detail": str(exc),
        },
    )


@app.exception_handler(ResourceNotFoundException)
async def resourceNotFoundExceptionHandler(
    request: Request,
    exc: ResourceNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "errorType": exc.__class__.__name__,
            "detail": str(exc),
        },
    )


@app.exception_handler(ConflictException)
async def conflictExceptionHandler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=409,
        content={
            "errorType": exc.__class__.__name__,
            "detail": str(exc),
        },
    )


@app.exception_handler(AuthenticationException)
async def authenticationExceptionHandler(
    request: Request,
    exc: AuthenticationException,
):
    return JSONResponse(
        status_code=401,
        content={
            "errorType": exc.__class__.__name__,
            "detail": str(exc),
        },
    )


@app.exception_handler(AuthorizationException)
async def authorizationExceptionHandler(
    request: Request,
    exc: AuthorizationException,
):
    return JSONResponse(
        status_code=403,
        content={
            "errorType": exc.__class__.__name__,
            "detail": str(exc),
        },
    )


@app.exception_handler(SecurityScanException)
async def securityScanExceptionHandler(
    request: Request,
    exc: SecurityScanException,
):
    return JSONResponse(
        status_code=503,
        content={
            "errorType": exc.__class__.__name__,
            "detail": str(exc),
        },
    )


@app.exception_handler(AppException)
async def appExceptionHandler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=500,
        content={
            "errorType": exc.__class__.__name__,
            "detail": str(exc),
        },
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "upload-input-service",
    }