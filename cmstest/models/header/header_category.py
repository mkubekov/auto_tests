"""Header category: a top-level menu entry that groups existing subcategories."""

from __future__ import annotations

from pydantic import BaseModel, Field

from cmstest.data.enums import HeaderActionType, MenuType
from cmstest.data.generators import fake
from cmstest.http.references import references
from cmstest.models.common import BaseFields, Reference


class NestedSubcategories(BaseModel):
    position: int = 0
    elementValue: str = "title"
    subcategories: list[Reference] = Field(
        default_factory=lambda: [references().first("header_subcategories")]
    )


class PositionedSubcategory(BaseModel):
    position: int = 1
    subcategory: Reference = Field(
        default_factory=lambda: references().first("header_subcategories")
    )


class HeaderCategory(BaseFields):
    menuType: MenuType | None = Field(default_factory=lambda: fake.random_element(MenuType))
    menuCategory: str = Field(default_factory=lambda: fake.word())
    actionType: HeaderActionType = Field(
        default_factory=lambda: fake.random_element(HeaderActionType)
    )
    link: str | None = Field(default_factory=lambda: fake.url())
    position: int | None = 1
    colorFill: bool = Field(default_factory=lambda: fake.boolean())
    subcategories: list[PositionedSubcategory] = Field(
        default_factory=lambda: [PositionedSubcategory()]
    )
    nestedElements: list[str] | None = Field(default_factory=list)
    nestedSubcategories: list[NestedSubcategories] = Field(
        default_factory=lambda: [NestedSubcategories()]
    )
