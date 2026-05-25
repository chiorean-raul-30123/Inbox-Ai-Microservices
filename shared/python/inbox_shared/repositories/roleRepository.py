from sqlalchemy import select
from sqlalchemy.orm import Session

from inbox_shared.models import Role


class RoleRepository:
    def getById(self, db: Session, roleId: int) -> Role | None:
        stmt = select(Role).where(Role.id == roleId)
        return db.execute(stmt).scalar_one_or_none()

    def getByName(self, db: Session, name: str) -> Role | None:
        stmt = select(Role).where(Role.name == name)
        return db.execute(stmt).scalar_one_or_none()

    def listAll(self, db: Session) -> list[Role]:
        stmt = select(Role).order_by(Role.id.asc())
        return list(db.execute(stmt).scalars().all())

    def create(
        self,
        db: Session,
        *,
        name: str,
        description: str | None = None,
    ) -> Role:
        role = Role(
            name=name,
            description=description,
        )

        db.add(role)
        db.commit()
        db.refresh(role)

        return role