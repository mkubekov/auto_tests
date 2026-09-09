"""Header category form: action type drives which sub-form is shown.

The nested-subcategory widgets were never exercised against a live admin panel; the
module carries a ``cms_skip_reason`` in the registry until they are verified.
"""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.data.enums import HeaderActionType, MenuType
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import DropDown


class HeaderCategory(CmsPage):
    _menu_category = '[id="menuCategory"]'
    _menu_type = '[id="menuType"]'
    _color_fill = '[id="colorFill"]'
    _subcategories = '[id="subcategories"]'

    @staticmethod
    def _nested_subcategories(index: int) -> str:
        return f'[id="nestedSubcategories_{index}_subcategories"]'

    def _fill_expand_menu(self, payload: dict[str, Any]) -> None:
        DropDown(self.page, "Menu type", self._menu_type).select(
            labels.MENU_TYPE[payload["menuType"]]
        )
        self.check("Colour fill", self._color_fill, payload["colorFill"])
        if payload["menuType"] == MenuType.FLAT:
            for entry in payload["subcategories"]:
                DropDown(self.page, "Subcategories", self._subcategories).set(
                    entry["subcategory"]["name"]
                )
        else:
            for index, nested in enumerate(payload["nestedSubcategories"]):
                for subcategory in nested["subcategories"]:
                    DropDown(
                        self.page, "Nested subcategories", self._nested_subcategories(index)
                    ).set(subcategory["name"])

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create header category"):
            self.fill_name(payload["name"])
            self.fill("Menu category", self._menu_category, payload["menuCategory"])
            self.fill("Position", self._position, payload["position"])
            DropDown(self.page, "Action", self._actionType).select(
                labels.HEADER_ACTION[payload["actionType"]]
            )
            if payload["actionType"] == HeaderActionType.EXPAND:
                self._fill_expand_menu(payload)
            else:
                self.fill("Link", self._link, payload["link"])
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_item("Menu category", payload["menuCategory"], created["menuCategory"])
        self.check_item("Position", payload["position"], created["position"])
        self.check_item("Action", payload["actionType"], created["actionType"])
        if payload["actionType"] == HeaderActionType.EXPAND:
            self.check_item("Menu type", payload["menuType"], created["menuType"])
            self.check_item("Colour fill", payload["colorFill"], created["colorFill"])
        else:
            self.check_item("Link", payload["link"], created["link"])
        return self
