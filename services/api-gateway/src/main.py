from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from inbox_shared.database.initDb import initDb
from inbox_shared.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConflictException,
    ResourceNotFoundException,
    ValidationException,
)
from src.api.router import apiRouter


app = FastAPI(title="Inbox AI API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    initDb()


@app.get("/")
def root():
    return {"message": "Inbox AI API Gateway running"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}


@app.exception_handler(ValidationException)
async def validationExceptionHandler(request: Request, exc: ValidationException):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(AuthenticationException)
async def authenticationExceptionHandler(request: Request, exc: AuthenticationException):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(ConflictException)
async def conflictExceptionHandler(request: Request, exc: ConflictException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(AuthorizationException)
async def authorizationExceptionHandler(request: Request, exc: AuthorizationException):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


@app.exception_handler(ResourceNotFoundException)
async def notFoundExceptionHandler(request: Request, exc: ResourceNotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


app.include_router(apiRouter)