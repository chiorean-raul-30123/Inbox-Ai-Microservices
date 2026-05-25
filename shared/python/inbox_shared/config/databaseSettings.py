import os
from dataclasses import dataclass


@dataclass
class DatabaseSettings:
    postgresUser: str = os.getenv("POSTGRES_USER", "inbox")
    postgresPassword: str = os.getenv("POSTGRES_PASSWORD", "inbox")
    postgresHost: str = os.getenv("POSTGRES_HOST", "localhost")
    postgresPort: int = int(os.getenv("POSTGRES_PORT", "5433"))
    postgresDb: str = os.getenv("POSTGRES_DB", "inbox_ai")

    @property
    def databaseUrl(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgresUser}:"
            f"{self.postgresPassword}@{self.postgresHost}:"
            f"{self.postgresPort}/{self.postgresDb}"
        )


databaseSettings = DatabaseSettings()