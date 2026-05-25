import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from inbox_shared.models import User


class UserRepository:
    def getById(self, db: Session, userId: uuid.UUID) -> User | None:
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .where(User.id == userId)
        )

        return db.execute(stmt).scalar_one_or_none()

    def getByEmail(self, db: Session, email: str) -> User | None:
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .where(User.email == email)
        )

        return db.execute(stmt).scalar_one_or_none()

    def listAll(self, db: Session) -> list[User]:
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .order_by(User.createdAt.desc())
        )

        return list(db.execute(stmt).scalars().all())

    def create(
        self,
        db: Session,
        *,
        fullName: str,
        email: str,
        passwordHash: str,
        roleId: int,
        isActive: bool = True,
    ) -> User:
        user = User(
            fullName=fullName,
            email=email,
            passwordHash=passwordHash,
            roleId=roleId,
            isActive=isActive,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def save(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user