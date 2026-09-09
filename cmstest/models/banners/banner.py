"""Site banner: images, rich text, buttons, targeting by category and city."""

from __future__ import annotations

from pydantic import Field

from cmstest.data.enums import BannerPosition
from cmstest.data.files import IMAGE_WEBP
from cmstest.data.generators import fake
from cmstest.http.references import references
from cmstest.models.common import BaseFields, Button, Tooltip


class Banner(BaseFields):
    active: bool = Field(default_factory=lambda: fake.boolean())
    analyticsId: str = Field(default_factory=lambda: fake.slug())
    backgroundColor: str = Field(default_factory=lambda: fake.color())
    backgroundImage: str = IMAGE_WEBP
    image: str = IMAGE_WEBP
    title: str | None = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    text: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    categories: list[str] | None = Field(
        default_factory=lambda: [references().value("categories", "value")]
    )
    cities: list[str] = Field(default_factory=lambda: [references().value("cities", "city")])
    buttons: list[Button] = Field(default_factory=lambda: [Button()])
    propagation: bool | None = Field(default_factory=lambda: fake.boolean())
    bannerPosition: BannerPosition = Field(
        default_factory=lambda: fake.random_element(BannerPosition)
    )
    isAdvertisement: bool = Field(default_factory=lambda: fake.boolean())
    tooltip: Tooltip | None = Field(default_factory=Tooltip)
