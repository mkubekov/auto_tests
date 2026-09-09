"""Repeatable "buttons" section present on many content blocks."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.components.dropdown import DropDown

if TYPE_CHECKING:
    from cmstest.pages.cms.base import CmsPage


class Buttons:
    """Adds and fills ``buttons[i]`` rows; ``prefix`` scopes ids for nested sections."""

    _add = '[id="add-button"]'

    def __init__(self, form: CmsPage, prefix: str = "") -> None:
        self.form = form
        self.prefix = prefix

    def _id(self, index: int, field: str) -> str:
        return f'[id="{self.prefix}buttons_{index}_{field}"]'

    def add(self) -> Self:
        self.form.click("Add button", self._add)
        return self

    def fill(self, button: dict[str, Any], index: int = 0) -> Self:
        if not button["active"]:
            return self
        with allure.step(f"Button {index + 1}"):
            self.add()
            self.form.switch("Active", self._id(index, "active"), button["active"])
            self.form.fill("Button text", self._id(index, "text"), button["text"])
            DropDown(self.form.page, "Button action", self._id(index, "actionType")).set(
                labels.BUTTON_ACTION[button["actionType"]], log=False
            )
            self.form.fill("Action value", self._id(index, "actionValue"), button["actionValue"])
            DropDown(self.form.page, "Button style", self._id(index, "style")).set_by_enter(
                labels.BUTTON_STYLE[button["style"]]
            )
        return self

    def check(self, sent: dict[str, Any], received: dict[str, Any]) -> Self:
        self.form.check_item("Button active", sent["active"], received["active"])
        self.form.check_item("Button text", sent["text"], received["text"])
        self.form.check_item("Button action", sent["actionType"], received["actionType"])
        self.form.check_item("Action value", sent["actionValue"], received["actionValue"])
        return self
