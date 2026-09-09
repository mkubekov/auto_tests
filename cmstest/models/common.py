"""Building blocks shared by request models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from cmstest.data.enums import ButtonAction, ButtonStyle
from cmstest.data.generators import fake, unique_name

# An existing entity referenced by the whole object the API returned for it. Kept as a plain
# mapping on purpose: the referenced entity is sent back exactly as the stand describes it.
Reference = dict[str, Any]


class BaseFields(BaseModel):
    """Fields every CMS entity has. ``name`` carries the run marker that cleanup searches for."""

    id: str | None = None
    createdAt: str | None = None
    updatedAt: str | None = None
    name: str = Field(default_factory=unique_name)


class Button(BaseModel):
    text: str = Field(default_factory=lambda: fake.text(max_nb_chars=15))
    style: ButtonStyle = Field(default_factory=lambda: fake.random_element(ButtonStyle))
    active: bool = True
    actionType: ButtonAction = ButtonAction.LINK
    actionValue: str = Field(default_factory=lambda: fake.url())
    backgroundColor: str | None = Field(default_factory=lambda: fake.color())


class Tooltip(BaseModel):
    title: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    text: str = Field(default_factory=lambda: fake.text(max_nb_chars=20))


def build_payload(model: type[BaseModel]) -> dict[str, Any]:
    """Instantiate a request model and dump it as a JSON-compatible dict.

    Takes the class, not an instance: field values come from ``default_factory`` at call
    time, so every call yields fresh Faker data.
    """
    return model().model_dump(mode="json", exclude_none=True, by_alias=True)
