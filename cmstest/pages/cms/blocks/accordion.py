"""Accordion form: category dropdown, colour scheme, repeatable items with rich text."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import DropDown, TextEditor


class Accordion(CmsPage):
    _block_color = '[id="blockColor"]'
    _add_item = "Add item"

    @staticmethod
    def _item_title(index: int) -> str:
        return f'[id="items_{index}_title"]'

    @staticmethod
    def _item_description(index: int) -> str:
        return f'[id="items_{index}_description"]'

    def select_category(self, value: str) -> Self:
        DropDown(self.page, "Category", self._category).set(value)
        return self

    def select_color(self, value: str) -> Self:
        DropDown(self.page, "Block colour", self._block_color).select(labels.BLOCK_COLOR[value])
        return self

    def add_item(self, index: int, item: dict[str, Any]) -> Self:
        with allure.step(f"Item {index + 1}"):
            self.click_dashed(self._add_item)
            TextEditor(self.page, "Item title", self._item_title(index)).type(item["title"])
            TextEditor(self.page, "Item description", self._item_description(index)).type(
                item["description"]
            )
        return self

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create accordion"):
            self.fill_name(payload["name"])
            self.select_category(payload["category"])
            TextEditor(self.page, "Title", self._title).type(payload["title"])
            self.select_color(payload["blockColor"])
            for index, item in enumerate(payload["items"]):
                self.add_item(index, item)
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_item("Category", payload["category"], created["category"])
        self.check_text("Title", payload["title"], created["title"])
        self.check_item("Block colour", payload["blockColor"], created["blockColor"])
        for index, item in enumerate(payload["items"]):
            with allure.step(f"Item {index + 1}"):
                got = created["items"][index]
                self.check_text("Item title", item["title"], got["title"])
                self.check_text("Item description", item["description"], got["description"])
        return self
