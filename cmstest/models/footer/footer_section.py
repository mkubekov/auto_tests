"""Footer section: a titled list of links."""

from __future__ import annotations

from pydantic import BaseModel, Field

from cmstest.data.generators import fake
from cmstest.models.common import BaseFields


class FooterLink(BaseModel):
    linkText: str = Field(default_factory=lambda: fake.word())
    link: str = Field(default_factory=lambda: fake.url())
    priority: str = "1"


class FooterSection(BaseFields):
    title: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    priority: str = "1"
    isShowTitle: bool = Field(default_factory=lambda: fake.boolean())
    links: list[FooterLink] = Field(default_factory=lambda: [FooterLink()])
