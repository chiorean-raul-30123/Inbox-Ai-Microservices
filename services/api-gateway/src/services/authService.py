from sqlalchemy.orm import Session

from inbox_shared.exceptions import (
    AuthenticationException,
    ConflictException,
    ValidationException,
)
from inbox_shared.models import User
from inbox_shared.repositories import RoleRepository, UserRepository
from src.core.security import createAccessToken, hashPassword, verifyPassword
from src.schemas.auth import LoginRequest, RegisterRequest


class AuthService:
    def __init__(
        self,
        userRepository: UserRepository,
        roleRepository: RoleRepository,
    ) -> None:
        self.userRepository = userRepository
        self.roleRepository = roleRepository

    def register(self, db: Session, request: RegisterRequest) -> User:
        existingUser = self.userRepository.getByEmail(db, request.email)

        if existingUser is not None:
            raise ConflictException("A user with this email already exists.")

        role = self.roleRepository.getById(db, request.roleId)

        if role is None:
            raise ValidationException("Invalid role_id.")

        passwordHash = hashPassword(request.password)

        return self.userRepository.create(
            db,
            fullName=request.fullName,
            email=request.email,
            passwordHash=passwordHash,
            roleId=request.roleId,
            isActive=True,
        )

    def login(self, db: Session, request: LoginRequest) -> str:
        user = self.userRepository.getByEmail(db, request.email)

        if user is None:
            raise AuthenticationException("Invalid email or password.")

        if not user.isActive:
            raise AuthenticationException("User account is inactive.")

        if not verifyPassword(request.password, user.passwordHash):
            raise AuthenticationException("Invalid email or password.")

        return createAccessToken(subject=str(user.id))