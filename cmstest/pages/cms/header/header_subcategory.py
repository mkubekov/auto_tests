"""Header subcategory form: list type drives the fields of each repeated item."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.data.enums import SubcategoryAction, SubcategoryType
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import DropDown


class HeaderSubcategory(CmsPage):
    _type = '[id="type"]'
    _add_item = "Add item"

    @staticmethod
    def _item(index: int, field: str) -> str:
        return f'[id="list_{index}_{field}"]'

    @staticmethod
    def _item_upload(index: int, field: str) -> str:
        return f'[for="list_{index}_{field}"]'

    def add_item(self, index: int, item: dict[str, Any], list_type: str) -> Self:
        with allure.step(f"Item {index + 1}"):
            self.click_dashed(self._add_item)
            if list_type == SubcategoryType.LIST:
                self.fill("Item text", self._item(index, "text"), item["title"])
            else:
                self.fill("Item title", self._item(index, "title"), item["title"])
                self.fill("Item subtitle", self._item(index, "subtitle"), item["subtitle"])
                self.upload("Item image", self._item_upload(index, "image"), item["image"])
            DropDown(self.page, "Item action", self._item(index, "actionType")).select(
                labels.SUBCATEGORY_ACTION[item["actionType"]]
            )
            if item["actionType"] == SubcategoryAction.LINK:
                self.fill("Item link", self._item(index, "link"), item["link"])
        return self

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create header subcategory"):
            self.fill_name(payload["name"])
            DropDown(self.page, "List type", self._type).select(
                labels.SUBCATEGORY_TYPE[payload["type"]]
            )
            self.fill("Title", self._title, payload["title"])
            DropDown(self.page, "Action", self._actionType).select(
                labels.SUBCATEGORY_ACTION[payload["actionType"]]
            )
            if payload["actionType"] == SubcategoryAction.LINK:
                self.fill("Link", self._link, payload["link"])
            for index, item in enumerate(payload["list"]):
                self.add_item(index, item, payload["type"])
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_item("List type", payload["type"], created["type"])
        self.check_item("Title", payload["title"], created["title"])
        self.check_item("Action", payload["actionType"], created["actionType"])
        if payload["actionType"] == SubcategoryAction.LINK:
            self.check_item("Link", payload["link"], created["link"])
        for index, item in enumerate(payload["list"]):
            with allure.step(f"Item {index + 1}"):
                got = created["list"][index]
                self.check_item("Item title", item["title"], got["title"])
                self.check_item("Item action", item["actionType"], got["actionType"])
        return self
