"""Video lessons page: hero section, SEO meta and a list of videos with labels."""

from __future__ import annotations

from pydantic import BaseModel, Field

from cmstest.data.files import IMAGE_WEBP
from cmstest.data.generators import fake
from cmstest.http.references import references
from cmstest.models.common import BaseFields


class HeroSection(BaseModel):
    title: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    subtitle: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    btnText: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    imageUrl: str = IMAGE_WEBP


class Meta(BaseModel):
    noIndex: bool = Field(default_factory=lambda: fake.boolean())
    title: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    description: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))


class VideoItem(BaseModel):
    title: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    description: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    videoLink: str = Field(default_factory=lambda: fake.url())
    imageLink: str = IMAGE_WEBP
    labels: list[str] = Field(default_factory=lambda: [references().value("labels", "value")])


class VideoLessons(BaseFields):
    noIndex: bool | None = Field(default_factory=lambda: fake.boolean())
    externalName: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    url: str | None = Field(default_factory=lambda: f"/video-lessons/{fake.slug()}")
    blockColor: str | None = Field(default_factory=lambda: fake.color())
    firstScreen: HeroSection | None = Field(default_factory=HeroSection)
    meta: Meta | None = Field(default_factory=Meta)
    videoTitle: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    videos: list[VideoItem] = Field(default_factory=lambda: [VideoItem()])
