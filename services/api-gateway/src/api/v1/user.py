import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from inbox_shared.database import getDb
from inbox_shared.enums import RoleType
from inbox_shared.models import User
from inbox_shared.repositories import RoleRepository, UserRepository
from src.api.deps import getCurrentActiveUser, requireRoles
from src.schemas.user import CreateUserRequest, UserResponse,ChangePasswordRequest
from src.services.userService import UserService



router = APIRouter(prefix="/users", tags=["Users"])


def getUserService() -> UserService:
    return UserService(
        userRepository=UserRepository(),
        roleRepository=RoleRepository(),
    )


@router.get("", response_model=list[UserResponse], response_model_by_alias=True)
def listUsers(
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN)),
    userService: UserService = Depends(getUserService),
):
    return userService.listUsers(db)


@router.post("", response_model=UserResponse, response_model_by_alias=True)
def createUser(
    request: CreateUserRequest,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN)),
    userService: UserService = Depends(getUserService),
):
    user = userService.createUser(db, request)
    return UserResponse.model_validate(user)


@router.delete("/{userId}", response_model=UserResponse, response_model_by_alias=True)
def deactivateUser(
    userId: uuid.UUID,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles(RoleType.ADMIN)),
    userService: UserService = Depends(getUserService),
):
    user = userService.deactivateUser(
        db,
        userId=userId,
        currentUserId=currentUser.id,
    )

    return UserResponse.model_validate(user)

@router.post("/me/change-password", response_model=UserResponse, response_model_by_alias=True)
def changeOwnPassword(
    request: ChangePasswordRequest,
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentActiveUser),
    userService: UserService = Depends(getUserService),
):
    user = userService.changeOwnPassword(
        db,
        currentUser=currentUser,
        request=request,
    )

    return UserResponse.model_validate(user)