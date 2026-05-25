from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from inbox_shared.config.databaseSettings import databaseSettings


engine = create_engine(
    databaseSettings.databaseUrl,
    connect_args={"options": "-c timezone=utc"},
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def createDbSession():
    return SessionLocal()