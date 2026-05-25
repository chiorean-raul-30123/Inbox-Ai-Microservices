from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from inbox_shared.database import getDb
from inbox_shared.models import User
from inbox_shared.repositories import RoleRepository, UserRepository
from src.api.deps import getCurrentActiveUser
from src.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from src.schemas.user import UserResponse
from src.services.authService import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


def getAuthService() -> AuthService:
    return AuthService(
        userRepository=UserRepository(),
        roleRepository=RoleRepository(),
    )


@router.post("/register", response_model=UserResponse, response_model_by_alias=True)
def register(
    request: RegisterRequest,
    db: Session = Depends(getDb),
    authService: AuthService = Depends(getAuthService),
):
    user = authService.register(db, request)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse, response_model_by_alias=True)
def login(
    request: LoginRequest,
    db: Session = Depends(getDb),
    authService: AuthService = Depends(getAuthService),
):
    token = authService.login(db, request)
    return TokenResponse(accessToken=token)


@router.get("/me", response_model=UserResponse, response_model_by_alias=True)
def getMe(
    currentUser: User = Depends(getCurrentActiveUser),
):
    return UserResponse.model_validate(currentUser)