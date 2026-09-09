"""Accordion block: expandable items, each with its own buttons."""

from __future__ import annotations

from pydantic import BaseModel, Field

from cmstest.data.enums import BlockColor
from cmstest.data.generators import fake
from cmstest.http.references import references
from cmstest.models.common import BaseFields, Button


class AccordionItem(BaseModel):
    title: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    description: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    buttons: list[Button] = Field(default_factory=lambda: [Button()])


class CustomColors(BaseModel):
    accentColor: str = Field(default_factory=lambda: fake.color())
    backgroundColor: str = Field(default_factory=lambda: fake.color())


class Accordion(BaseFields):
    category: str = Field(default_factory=lambda: references().value("categories", "value"))
    title: str | None = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    blockColor: BlockColor = Field(default_factory=lambda: fake.random_element(BlockColor))
    customColors: CustomColors | None = Field(default_factory=CustomColors)
    items: list[AccordionItem] = Field(default_factory=lambda: [AccordionItem()])
    buttons: list[Button] | None = Field(default_factory=lambda: [Button()])
