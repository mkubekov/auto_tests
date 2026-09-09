"""Footer section form: title, position and a repeatable list of links."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.base import CmsPage


class FooterSection(CmsPage):
    _is_show_title = '[id="isShowTitle"]'
    _add_link = "Add link"

    @staticmethod
    def _link_field(index: int, field: str) -> str:
        return f'[id="links_{index}_{field}"]'

    def add_link(self, index: int, link: dict[str, Any]) -> Self:
        with allure.step(f"Link {index + 1}"):
            self.click_dashed(self._add_link)
            self.fill("Link text", self._link_field(index, "linkText"), link["linkText"])
            self.fill("Link", self._link_field(index, "link"), link["link"])
            self.fill("Link priority", self._link_field(index, "priority"), link["priority"])
        return self

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create footer section"):
            self.fill_name(payload["name"])
            self.fill("Title", self._title, payload["title"])
            self.fill("Priority", self._priority, payload["priority"])
            self.switch("Show title", self._is_show_title, payload["isShowTitle"])
            for index, link in enumerate(payload["links"]):
                self.add_link(index, link)
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_item("Title", payload["title"], created["title"])
        self.check_item("Priority", payload["priority"], created["priority"])
        self.check_item("Show title", payload["isShowTitle"], created["isShowTitle"])
        for index, link in enumerate(payload["links"]):
            with allure.step(f"Link {index + 1}"):
                got = created["links"][index]
                self.check_item("Link text", link["linkText"], got["linkText"])
                self.check_item("Link", link["link"], got["link"])
                self.check_item("Link priority", link["priority"], got["priority"])
        return self
