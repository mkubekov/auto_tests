"""Quill rich-text editor wrapper."""

from __future__ import annotations

from typing import Self

import allure
from playwright.sync_api import Page

from cmstest.data.enums import Font


class TextEditor:
    def __init__(self, page: Page, caption: str, locator: str) -> None:
        self.page = page
        self.caption = caption
        self.root = page.locator(locator)

    def type(self, value: str) -> Self:
        with allure.step(f'Fill "{self.caption}": {value}'):
            self.root.locator(".ql-editor").fill(value)
        return self

    def _toolbar(self, caption: str, locator: str) -> Self:
        with allure.step(f"{self.caption}: {caption}"):
            self.root.locator(locator).click()
        return self

    def heading(self, level: int) -> Self:
        return self._toolbar(f"heading {level}", f'[value="{level}"]')

    def bold(self) -> Self:
        return self._toolbar("bold", ".ql-bold")

    def italic(self) -> Self:
        return self._toolbar("italic", ".ql-italic")

    def underline(self) -> Self:
        return self._toolbar("underline", ".ql-underline")

    def strike(self) -> Self:
        return self._toolbar("strike", ".ql-strike")

    def ordered_list(self) -> Self:
        return self._toolbar("ordered list", '[value="ordered"]')

    def bullet_list(self) -> Self:
        return self._toolbar("bullet list", '[value="bullet"]')

    def link(self) -> Self:
        return self._toolbar("link", ".ql-link")

    def clear_formatting(self) -> Self:
        return self._toolbar("clear formatting", ".ql-clean")

    def text_color(self, value: str) -> Self:
        with allure.step(f"{self.caption}: text colour {value}"):
            self.root.locator(".ql-color-picker").nth(0).click()
            self.root.locator(f'[data-value="{value}"]').click()
        return self

    def background_color(self, value: str) -> Self:
        with allure.step(f"{self.caption}: background colour {value}"):
            self.root.locator(".ql-color-picker").nth(1).click()
            self.root.locator(f'[data-value="{value}"]').click()
        return self

    def font(self, value: Font) -> Self:
        with allure.step(f"{self.caption}: font {value}"):
            self.root.locator(".ql-font").click()
            self.root.locator(f'[data-value="{value}"]').click()
        return self
