"""Text block: the smallest page-constructor template."""

from __future__ import annotations

from pydantic import Field

from cmstest.data.generators import fake
from cmstest.models.common import BaseFields


class TextBlock(BaseFields):
    text: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
