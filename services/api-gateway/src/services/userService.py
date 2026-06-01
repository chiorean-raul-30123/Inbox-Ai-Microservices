import uuid

from sqlalchemy.orm import Session

from inbox_shared.exceptions import ConflictException, ResourceNotFoundException, ValidationException,AuthenticationException
from inbox_shared.models import User
from inbox_shared.repositories import RoleRepository, UserRepository
from src.core.security import hashPassword
from src.schemas.user import CreateUserRequest 
from src.core.security import hashPassword, verifyPassword
from src.schemas.user import ChangePasswordRequest


class UserService:
    def __init__(
        self,
        userRepository: UserRepository,
        roleRepository: RoleRepository,
    ) -> None:
        self.userRepository = userRepository
        self.roleRepository = roleRepository

    def listUsers(self, db: Session) -> list[User]:
        return self.userRepository.listAll(db)

    def createUser(self, db: Session, request: CreateUserRequest) -> User:
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

    def deactivateUser(
        self,
        db: Session,
        userId: uuid.UUID,
        currentUserId: uuid.UUID,
    ) -> User:
        user = self.userRepository.getById(db, userId)

        if user is None:
            raise ResourceNotFoundException("User not found.")

        if user.id == currentUserId:
            raise ValidationException("You cannot deactivate your own account.")

        user.isActive = False

        return self.userRepository.save(db, user)
    
    def changeOwnPassword(
        self,
        db: Session,
        currentUser: User,
        request: ChangePasswordRequest,
    ) -> User:
        if not verifyPassword(request.currentPassword, currentUser.passwordHash):
            raise ValidationException("Current password is incorrect.")

        if verifyPassword(request.newPassword, currentUser.passwordHash):
            raise ValidationException("New password must be different from current password.")

        currentUser.passwordHash = hashPassword(request.newPassword)

        return self.userRepository.save(db, currentUser)