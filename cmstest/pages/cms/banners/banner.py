"""Banner form: two uploads, rich text, buttons, multi-select targeting, switches."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import Buttons, DropDown, TextEditor


class Banner(CmsPage):
    _analytics_id = '[id="analyticsId"]'
    _active = '[id="active"]'
    _is_advertisement = '[id="isAdvertisement"]'
    _tooltip_title = '[id="tooltip.title"]'
    _tooltip_text = '[id="tooltip.text"]'
    _text = '[class="quill "]'
    _background_image = '[for="backgroundImage"]'
    _banner_position = '[id="bannerPosition"]'
    _propagation = '[id="propagation"]'

    def __init__(self, page) -> None:
        super().__init__(page)
        self.buttons = Buttons(self)

    def fill_tooltip(self, tooltip: dict[str, Any]) -> Self:
        self.fill("Tooltip title", self._tooltip_title, tooltip["title"])
        self.fill("Tooltip text", self._tooltip_text, tooltip["text"])
        return self

    def select_category(self, value: str) -> Self:
        DropDown(self.page, "Category", self._categories).set(value)
        return self

    def select_position(self, value: str) -> Self:
        DropDown(self.page, "Position", self._banner_position).select(labels.BANNER_POSITION[value])
        return self

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create banner"):
            self.fill_name(payload["name"])
            self.fill("Analytics id", self._analytics_id, payload["analyticsId"])
            self.switch("Active", self._active, payload["active"])
            self.switch("Advertisement", self._is_advertisement, payload["isAdvertisement"])
            if payload["isAdvertisement"]:
                self.fill_tooltip(payload["tooltip"])
            TextEditor(self.page, "Text", self._text).type(payload["text"])
            self.upload("Background image", self._background_image, payload["backgroundImage"])
            self.upload("Image", self._image, payload["image"])
            for index, button in enumerate(payload["buttons"]):
                self.buttons.fill(button, index)
            for category in payload.get("categories") or []:
                self.select_category(category)
            self.select_position(payload["bannerPosition"])
            self.switch("Propagate to child pages", self._propagation, payload["propagation"])
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_item("Analytics id", payload["analyticsId"], created["analyticsId"])
        self.check_item("Active", payload["active"], created["active"])
        self.check_item("Advertisement", payload["isAdvertisement"], created["isAdvertisement"])
        if payload["isAdvertisement"]:
            self.check_item(
                "Tooltip title", payload["tooltip"]["title"], created["tooltip"]["title"]
            )
            self.check_item("Tooltip text", payload["tooltip"]["text"], created["tooltip"]["text"])
        self.check_text("Text", payload["text"], created["text"])
        self.check_file("Background image", payload["backgroundImage"], created["backgroundImage"])
        self.check_file("Image", payload["image"], created["image"])
        for index, button in enumerate(payload["buttons"]):
            with allure.step(f"Button {index + 1}"):
                self.buttons.check(button, created["buttons"][index])
        for index, category in enumerate(payload.get("categories") or []):
            self.check_item("Category", category, created["categories"][index])
        self.check_item("Position", payload["bannerPosition"], created["bannerPosition"])
        return self
