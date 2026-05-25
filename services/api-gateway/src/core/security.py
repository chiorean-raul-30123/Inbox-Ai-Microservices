from datetime import datetime, timedelta, timezone
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from jose import JWTError, jwt

from inbox_shared.exceptions import AuthenticationException
from src.core.config import settings


passwordHasher = PasswordHasher()


def hashPassword(password: str) -> str:
    return passwordHasher.hash(password)


def verifyPassword(plainPassword: str, passwordHash: str) -> bool:
    try:
        return passwordHasher.verify(passwordHash, plainPassword)
    except (VerifyMismatchError, InvalidHashError):
        return False


def createAccessToken(subject: str, expiresDelta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expiresDelta or timedelta(minutes=settings.accessTokenExpireMinutes)
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwtSecretKey,
        algorithm=settings.jwtAlgorithm,
    )


def decodeToken(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.jwtSecretKey,
            algorithms=[settings.jwtAlgorithm],
        )
    except JWTError as exception:
        raise AuthenticationException("Invalid or expired token.") from exception


def extractSubjectFromToken(token: str) -> str:
    payload = decodeToken(token)
    subject = payload.get("sub")

    if not subject:
        raise AuthenticationException("Token subject is missing.")

    return subject