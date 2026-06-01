from io import BytesIO
from typing import Any

import httpx
from fastapi import UploadFile


class MailpitClient:
    def __init__(
        self,
        baseUrl: str = "http://localhost:8025",
    ) -> None:
        self.baseUrl = baseUrl.rstrip("/")

    def getMessage(self, messageId: str) -> dict[str, Any]:
        response = httpx.get(
            f"{self.baseUrl}/api/v1/message/{messageId}",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def getAttachmentFile(
        self,
        messageId: str,
        partId: str,
        filename: str,
        contentType: str,
    ) -> UploadFile:
        response = httpx.get(
            f"{self.baseUrl}/api/v1/message/{messageId}/part/{partId}",
            timeout=20,
        )
        response.raise_for_status()

        return UploadFile(
            filename=filename,
            file=BytesIO(response.content),
            headers={"content-type": contentType},
        )