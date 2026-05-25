from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from inbox_shared.database import Base
from inbox_shared.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class SystemSettings(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "system_settings"

    key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    value: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )