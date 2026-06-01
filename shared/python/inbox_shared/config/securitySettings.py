import os


class SecuritySettings:
    clamavHost: str = os.getenv("CLAMAV_HOST", "localhost")
    clamavPort: int = int(os.getenv("CLAMAV_PORT", "3310"))
    clamavEnabled: bool = os.getenv("CLAMAV_ENABLED", "true").lower() == "true"


securitySettings = SecuritySettings()