"""Gallery block: slides with media, buttons and per-breakpoint content offsets."""

from __future__ import annotations

from pydantic import BaseModel, Field

from cmstest.data.files import IMAGE_WEBP
from cmstest.data.generators import fake
from cmstest.models.common import BaseFields, Button, Tooltip


def _px(low: int, high: int) -> str:
    return f"{fake.pyint(low, high)}px"


class Offset(BaseModel):
    mobile: str = Field(default_factory=lambda: _px(320, 500))
    pad: str = Field(default_factory=lambda: _px(500, 750))
    tablet: str = Field(default_factory=lambda: _px(750, 1000))
    desktop: str = Field(default_factory=lambda: _px(1000, 1500))
    fullHD: str = Field(default_factory=lambda: _px(1500, 2000))
    ultraHD: str = Field(default_factory=lambda: _px(2000, 2500))


class GalleryItem(BaseModel):
    buttons: list[Button] = Field(default_factory=lambda: [Button()])
    src: str = Field(default_factory=lambda: fake.url())
    previewImageSrc: str = IMAGE_WEBP
    duration: int = Field(default_factory=lambda: fake.pyint(min_value=1000, max_value=2000))
    text: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    title: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    offset: Offset = Field(default_factory=Offset)
    isAdvertisement: bool = Field(default_factory=lambda: fake.boolean())
    tooltip: Tooltip = Field(default_factory=Tooltip)


class GalleryBlock(BaseFields):
    galleryList: list[GalleryItem] = Field(default_factory=lambda: [GalleryItem()])
