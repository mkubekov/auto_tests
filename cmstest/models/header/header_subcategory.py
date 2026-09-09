"""Header subcategory: the leaf level of the navigation menu."""

from __future__ import annotations

from pydantic import BaseModel, Field

from cmstest.data.enums import SubcategoryAction, SubcategoryType
from cmstest.data.files import IMAGE_WEBP
from cmstest.data.generators import fake
from cmstest.models.common import BaseFields


class SubcategoryItem(BaseModel):
    title: str | None = Field(default_factory=lambda: fake.word())
    actionType: SubcategoryAction = Field(
        default_factory=lambda: fake.random_element(SubcategoryAction)
    )
    link: str | None = Field(default_factory=lambda: fake.url())
    image: str | None = IMAGE_WEBP
    subtitle: str | None = Field(default_factory=lambda: fake.word())


class HeaderSubcategory(BaseFields):
    title: str | None = Field(default_factory=lambda: fake.text(max_nb_chars=20))
    type: SubcategoryType = Field(default_factory=lambda: fake.random_element(SubcategoryType))
    actionType: SubcategoryAction | None = Field(
        default_factory=lambda: fake.random_element(SubcategoryAction)
    )
    link: str | None = Field(default_factory=lambda: fake.url())
    # The API names this field ``list``; aliasing keeps the Python attribute meaningful.
    items: list[SubcategoryItem] | None = Field(
        alias="list", default_factory=lambda: [SubcategoryItem(), SubcategoryItem()]
    )
