from inbox_shared.database import Base, engine

from inbox_shared.models import (  
    AuditLog,
    Document,
    DocumentAssignment,
    DocumentPrediction,
    IncomingEmail,
    Role,
    SystemSettings,
    User,
)


def initDb():
    Base.metadata.create_all(bind=engine)