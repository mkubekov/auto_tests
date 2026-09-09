"""Promo banner form: colour picker, responsive images, audience.

The activity-period date-range picker is not automated yet; the module carries a
``cms_skip_reason`` in the registry until it is.
"""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import ColorPicker, DropDown


class PromoBanner(CmsPage):
    _banner_position = '[id="bannerPosition"]'
    _color = '[for="color"]'
    _image_web = '[for="images_web"]'
    _image_tablet = '[for="images_tablet"]'
    _image_mobile = '[for="images_mobile"]'
    _button_text = '[id="button_text"]'
    _button_link = '[id="button_link"]'
    _button_style = '[id="button_style"]'
    _audience = '[id="audience"]'

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create promo banner"):
            self.fill_name(payload["name"])
            DropDown(self.page, "Position", self._banner_position).select(
                labels.PROMO_BANNER_POSITION[payload["bannerPosition"]]
            )
            ColorPicker(self).set("Banner colour", self._color, payload["color"])
            images = payload["images"]
            self.upload("Image (web)", self._image_web, images["web"])
            self.upload("Image (tablet)", self._image_tablet, images["tablet"])
            self.upload("Image (mobile)", self._image_mobile, images["mobile"])
            button = payload["button"]
            self.fill("Button text", self._button_text, button["text"])
            self.fill("Button link", self._button_link, button["link"])
            DropDown(self.page, "Button style", self._button_style).select(
                labels.PROMO_BUTTON_STYLE[button["style"]]
            )
            # TODO: activity period (Ant RangePicker) is not automated; see registry skip reason.
            for audience in payload["audience"]:
                DropDown(self.page, "Audience", self._audience).select(labels.AUDIENCE[audience])
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_item("Position", payload["bannerPosition"], created["bannerPosition"])
        for key in ("web", "tablet", "mobile"):
            self.check_file(f"Image ({key})", payload["images"][key], created["images"][key])
        self.check_item("Button text", payload["button"]["text"], created["button"]["text"])
        self.check_item("Button link", payload["button"]["link"], created["button"]["link"])
        self.check_item("Button style", payload["button"]["style"], created["button"]["style"])
        self.check_item("Audience", payload["audience"], created["audience"])
        return self
