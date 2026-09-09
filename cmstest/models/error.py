"""Error envelope the API returns for 4xx responses."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """All fields are required on purpose: negative tests must fail on a bare ``{}``."""

    statusCode: int | str
    response: dict[str, Any] | str
    timestamp: str
    path: str
