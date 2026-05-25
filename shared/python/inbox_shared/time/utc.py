from datetime import datetime, timezone


def utcNowIso() -> str:
    return datetime.now(timezone.utc).isoformat()