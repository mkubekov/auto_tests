"""Promo banner shown to a chosen audience for a limited period."""

from __future__ import annotations

from pydantic import BaseModel, Field

from cmstest.data.enums import Audience, PromoBannerPosition, PromoButtonStyle
from cmstest.data.files import IMAGE_WEBP
from cmstest.data.generators import fake
from cmstest.models.common import BaseFields


class PromoButton(BaseModel):
    link: str = Field(default_factory=lambda: fake.url())
    text: str = Field(default_factory=lambda: fake.word())
    color: str = Field(default_factory=lambda: fake.color())
    style: PromoButtonStyle = Field(default_factory=lambda: fake.random_element(PromoButtonStyle))


class ResponsiveImages(BaseModel):
    web: str = IMAGE_WEBP
    tablet: str = IMAGE_WEBP
    mobile: str = IMAGE_WEBP


class ActivityPeriod(BaseModel):
    dateOfStart: str = Field(default_factory=lambda: fake.date_this_year().isoformat())
    dateOfEnd: str = Field(default_factory=lambda: fake.future_date(end_date="+90d").isoformat())


class PromoBanner(BaseFields):
    bannerPosition: PromoBannerPosition = Field(
        default_factory=lambda: fake.random_element(PromoBannerPosition)
    )
    color: str = Field(default_factory=lambda: fake.color())
    images: ResponsiveImages = Field(default_factory=ResponsiveImages)
    button: PromoButton = Field(default_factory=PromoButton)
    activityPeriod: ActivityPeriod = Field(default_factory=ActivityPeriod)
    audience: list[Audience] = Field(default_factory=lambda: [fake.random_element(Audience)])
