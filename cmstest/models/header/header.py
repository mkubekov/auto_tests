"""Site header: logo, buttons and existing categories referenced by object."""

from __future__ import annotations

from pydantic import Field

from cmstest.data.files import IMAGE_WEBP
from cmstest.http.references import references
from cmstest.models.common import BaseFields, Button, Reference


class Header(BaseFields):
    logoImage: str = IMAGE_WEBP
    buttons: list[Button] | None = Field(default_factory=lambda: [Button()])
    categories: list[Reference] = Field(
        default_factory=lambda: [references().first("header_categories")]
    )
