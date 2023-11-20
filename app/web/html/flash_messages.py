from enum import Enum
from typing import cast

from fastapi import Request
from pydantic import BaseModel

MESSAGES = "_messages"


class FlashCategory(str, Enum):
    ERROR = "error"
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"


class FlashMessage(BaseModel):
    msg: str
    category: FlashCategory = FlashCategory.INFO
    timeout: int | None = None

    def flash(self, request: Request) -> None:
        if MESSAGES not in request.session:
            request.session[MESSAGES] = []
        request.session[MESSAGES].append(self.model_dump())


def get_flashed_messages(request: Request) -> list[FlashMessage]:
    message = cast(list[dict], request.session.pop(MESSAGES, []))
    return [FlashMessage(**msg) for msg in message]
