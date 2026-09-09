"""Base page object for the public site.

The site layer is a scaffold: locators depend on the project's front-end and must be
provided per project. Assertions use Playwright's auto-waiting ``expect``.
"""

from __future__ import annotations

from typing import Any, Self

import allure
from bs4 import BeautifulSoup
from playwright.sync_api import Page, expect


class SitePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, url: str) -> Self:
        with allure.step(f"Open {url}"):
            self.page.goto(url)
        return self

    def click(self, caption: str, locator: str) -> Self:
        with allure.step(f'Click "{caption}"'):
            self.page.locator(locator).click()
        return self

    def click_text(self, caption: str, locator: str, text: str) -> Self:
        with allure.step(f'Click "{caption}" with text "{text}"'):
            self.page.locator(locator).get_by_text(text).first.click()
        return self

    def hover(self, text: str) -> Self:
        with allure.step(f'Hover "{text}"'):
            self.page.get_by_text(text).hover()
        return self

    def expect_text(self, caption: str, locator: str, expected: str) -> Self:
        """Expect the rendered text of ``locator``; ``expected`` may contain editor markup."""
        text = BeautifulSoup(expected, "html.parser").get_text()
        with allure.step(f'"{caption}" shows "{text}"'):
            expect(self.page.locator(locator)).to_have_text(text)
        return self

    def expect_visible(self, caption: str, locator: str) -> Self:
        with allure.step(f'"{caption}" is visible'):
            expect(self.page.locator(locator)).to_be_visible()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        raise NotImplementedError
