import uuid
from collections.abc import Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from inbox_shared.database import getDb
from inbox_shared.enums import RoleType
from inbox_shared.exceptions import AuthenticationException, AuthorizationException
from inbox_shared.models import User
from inbox_shared.repositories import UserRepository
from src.core.security import extractSubjectFromToken


bearerScheme = HTTPBearer()


def getUserRepository() -> UserRepository:
    return UserRepository()


def getCurrentUser(
    credentials: HTTPAuthorizationCredentials = Depends(bearerScheme),
    db: Session = Depends(getDb),
    userRepository: UserRepository = Depends(getUserRepository),
) -> User:
    token = credentials.credentials
    subject = extractSubjectFromToken(token)

    try:
        userId = uuid.UUID(subject)
    except ValueError as exception:
        raise AuthenticationException("Invalid token subject.") from exception

    user = userRepository.getById(db, userId)

    if user is None:
        raise AuthenticationException("User not found.")

    return user


def getCurrentActiveUser(
    currentUser: User = Depends(getCurrentUser),
) -> User:
    if not currentUser.isActive:
        raise AuthenticationException("User account is inactive.")

    return currentUser


def requireRoles(*allowedRoles: RoleType) -> Callable:
    def roleChecker(
        currentUser: User = Depends(getCurrentActiveUser),
    ) -> User:
        if currentUser.role is None:
            raise AuthorizationException("User has no assigned role.")

        allowedRoleValues = [role.value for role in allowedRoles]

        if currentUser.role.name not in allowedRoleValues:
            raise AuthorizationException("You are not allowed to access this resource.")

        return currentUser

    return roleChecker