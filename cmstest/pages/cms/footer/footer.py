"""Footer form: pick existing sections from a multi-select."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import DropDown


class Footer(CmsPage):
    _sections = '[id="sections"]'

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create footer"):
            self.fill_name(payload["name"])
            for section in payload["sections"]:
                DropDown(self.page, "Section", self._sections).set(section["name"])
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        for index, section in enumerate(payload["sections"]):
            self.check_item("Section", section["name"], created["sections"][index]["name"])
        return self
