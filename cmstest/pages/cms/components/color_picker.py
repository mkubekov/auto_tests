"""Ant Design ``ColorPicker`` wrapper.

Ported without a live admin panel to verify against: the DOM of the popover (hex input,
preset swatches) is assumed from Ant Design v5 defaults.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

import allure
from playwright.sync_api import expect

if TYPE_CHECKING:
    from cmstest.pages.cms.base import CmsPage


class ColorPicker:
    _hex_input = ".ant-color-picker-input input"
    _preset = ".ant-color-picker-presets-color"

    def __init__(self, form: CmsPage) -> None:
        self.form = form

    def set(self, caption: str, locator: str, value: str) -> Self:
        """Open the picker anchored at ``locator`` and enter ``value`` (``#rrggbb``)."""
        with allure.step(f'Set colour "{caption}": {value}'):
            trigger = (
                self.form.page.locator(locator)
                .locator("../..")
                .locator(".ant-form-item-control-input")
            )
            trigger.click()
            hex_input = self.form.page.locator(self._hex_input)
            expect(hex_input).to_be_visible()
            hex_input.fill(value.lstrip("#"))
            hex_input.press("Enter")
            trigger.click()  # close the popover
        return self
