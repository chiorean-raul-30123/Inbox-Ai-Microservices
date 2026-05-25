from sqlalchemy import select
from sqlalchemy.orm import Session

from inbox_shared.models import SystemSettings


class SystemSettingsRepository:
    def getByKey(self, db: Session, key: str) -> SystemSettings | None:
        stmt = select(SystemSettings).where(SystemSettings.key == key)
        return db.execute(stmt).scalar_one_or_none()

    def createSettings(
        self,
        db: Session,
        *,
        key: str,
        value: str,
        description: str | None = None,
    ) -> SystemSettings:
        settings = SystemSettings(
            key=key,
            value=value,
            description=description,
        )

        db.add(settings)
        db.commit()
        db.refresh(settings)

        return settings

    def updateSettings(
        self,
        db: Session,
        *,
        settings: SystemSettings,
        value: str,
        description: str | None = None,
    ) -> SystemSettings:
        settings.value = value

        if description is not None:
            settings.description = description

        db.add(settings)
        db.commit()
        db.refresh(settings)

        return settings