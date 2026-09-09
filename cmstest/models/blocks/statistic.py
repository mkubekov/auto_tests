"""Statistics block: a heading and a fixed set of metric cards."""

from __future__ import annotations

from pydantic import BaseModel, Field

from cmstest.data.generators import fake
from cmstest.http.references import references
from cmstest.models.common import BaseFields


class StatItem(BaseModel):
    title: str = Field(default_factory=lambda: f"{fake.random_int(1, 99)}%")
    text: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))


class Statistic(BaseFields):
    categories: list[str] = Field(
        default_factory=lambda: [references().value("categories", "value")]
    )
    title: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    subtitle: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    statBlocks: list[StatItem] = Field(default_factory=lambda: [StatItem() for _ in range(4)])
