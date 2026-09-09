"""Header form: logo upload and existing categories picked from a multi-select."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import DropDown


class Header(CmsPage):
    _logo = '[for="logoImage"]'

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create header"):
            self.fill_name(payload["name"])
            self.upload("Logo", self._logo, payload["logoImage"])
            for category in payload["categories"]:
                DropDown(self.page, "Categories", self._categories).set(category["menuCategory"])
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_file("Logo", payload["logoImage"], created["logoImage"])
        for index, category in enumerate(payload["categories"]):
            self.check_item("Category", category["name"], created["categories"][index]["name"])
        return self
