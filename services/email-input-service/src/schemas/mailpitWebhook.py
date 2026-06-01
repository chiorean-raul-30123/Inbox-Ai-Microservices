from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MailpitWebhookRequest(BaseModel):
    id: str | None = Field(default=None, alias="ID")
    messageId: str | None = Field(default=None, alias="MessageID")
    event: str | None = Field(default=None, alias="Event")

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    def getMessageId(self) -> str:
        if self.id:
            return self.id

        if self.messageId:
            return self.messageId

        raise ValueError("Mailpit webhook payload does not contain a message id.")