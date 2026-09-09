"""Reference dictionary row. One endpoint serves every dictionary; ``type`` selects it."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from cmstest.data.enums import HandbookType
from cmstest.data.generators import fake
from cmstest.models.common import BaseFields


class Handbook(BaseFields):
    type: HandbookType = Field(default_factory=lambda: fake.random_element(HandbookType))
    value: str = Field(default_factory=lambda: f"/{fake.slug()}")
    extraFields: dict[str, Any] = Field(default_factory=dict)
