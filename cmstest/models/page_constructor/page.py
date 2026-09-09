"""Page template: the container that composes blocks by type and template id."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from cmstest.data.generators import fake
from cmstest.http.references import references
from cmstest.models.common import BaseFields


class Breadcrumb(BaseModel):
    name: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    path: str = Field(default_factory=lambda: f"/{fake.slug()}")


class PageBlock(BaseModel):
    """One slot of the page. ``blockTemplateId`` is a placeholder until a test replaces it
    with the id of a block it created (see the ``page_with_block`` fixture)."""

    blockType: str = "textBlock"
    scrollId: str = Field(default_factory=lambda: fake.slug())
    priority: int = 10
    inlineBlockData: dict[str, Any] | None = Field(default_factory=dict)
    noMargin: bool = Field(default_factory=lambda: fake.boolean())
    topOffset: str = "default"
    bottomOffset: str = "default"
    blockFill: bool = Field(default_factory=lambda: fake.boolean())
    blockFillColor: str = Field(default_factory=lambda: fake.color())
    blockTemplateId: str | None = Field(default_factory=lambda: str(uuid4()))
    cities: list[str] = Field(default_factory=lambda: [references().value("cities", "city")])


class Page(BaseFields):
    isActive: bool = Field(default_factory=lambda: fake.boolean())
    cities: list[str] = Field(default_factory=lambda: [references().value("cities", "city")])
    url: str = Field(default_factory=lambda: fake.slug())
    metaTitle: str | None = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    metaDescription: str | None = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    noIndex: bool | None = Field(default_factory=lambda: fake.boolean())
    hasMicroMarkup: bool | None = Field(default_factory=lambda: fake.boolean())
    breadcrumbs: list[Breadcrumb] = Field(default_factory=lambda: [Breadcrumb()])
    blocks: list[PageBlock] = Field(default_factory=lambda: [PageBlock()])
