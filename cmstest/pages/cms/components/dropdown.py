"""Ant Design ``Select`` wrapper."""

from __future__ import annotations

from collections.abc import Callable
from typing import Self

import allure
from playwright.sync_api import Locator, Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# Upper bound for walking a list with ArrowDown; enum-like lists are far shorter.
MAX_SCAN_STEPS = 50
# How long to wait for the highlighted option to move after a key press.
SCAN_STEP_TIMEOUT_MS = 1_000


class DropDown:
    """Two selection strategies for Ant's virtualised dropdown.

    * :meth:`set` types the value to filter the list and picks the highlighted option.
      Works for long reference lists (cities, categories) because the virtual list only
      renders the rows that are visible.
    * :meth:`select` opens the list and walks it with ArrowDown until an option's label
      matches. Only for short, enum-like lists.
    """

    def __init__(self, page: Page, caption: str, locator: str) -> None:
        self.page = page
        self.caption = caption
        self.element = page.locator(locator)

    @property
    def _listbox(self) -> Locator:
        """Ant renders the option list as ``<select id>_list`` next to a virtual list."""
        element_id = self.element.get_attribute("id")
        return self.page.locator(f'[id="{element_id}_list"] + .rc-virtual-list')

    @property
    def _active_option(self) -> Locator:
        return self._listbox.locator(".ant-select-item-option-active")

    def _run(self, value: str, action: Callable[[], None], log: bool) -> Self:
        if log:
            with allure.step(f'Select "{self.caption}": {value}'):
                action()
        else:
            action()
        return self

    def set(self, value: str, *, log: bool = True) -> Self:
        def action() -> None:
            self.element.click()
            self.element.fill(value)
            expect(self._active_option).to_be_visible()
            self._active_option.click()

        return self._run(value, action, log)

    def set_by_enter(self, value: str, *, log: bool = True) -> Self:
        def action() -> None:
            self.element.fill(value)
            self.element.press("Enter")

        return self._run(value, action, log)

    def select(self, label: str, *, log: bool = True) -> Self:
        def action() -> None:
            self.element.press("Enter")
            self._scan(
                lambda option: label
                in {option.get_attribute("title"), option.get_attribute("label")}
            )

        return self._run(label, action, log)

    def select_by_text(self, text: str, *, log: bool = True) -> Self:
        def action() -> None:
            self.element.click()
            self._scan(lambda option: option.text_content() == text)

        return self._run(text, action, log)

    def wait_loaded(self) -> Self:
        """Wait until the async options finished loading (Ant shows a spinner meanwhile)."""
        expect(self.page.locator(".ant-spin")).to_be_hidden()
        return self

    def add_option(self, value: str) -> Self:
        """Create a new option through the inline "add" form at the bottom of the list."""
        footer = self.page.locator(f'[id="{self.element.get_attribute("id")}_list"]').locator("..")
        footer.locator('[type="text"]').fill(value)
        footer.get_by_text("Add").click()
        return self

    def _scan(self, matches: Callable[[Locator], bool]) -> None:
        """Walk the options with ArrowDown until ``matches`` accepts the highlighted one."""
        expect(self._active_option).to_be_visible()
        for _ in range(MAX_SCAN_STEPS):
            option = self._active_option
            if matches(option):
                option.click()
                return
            previous = option.text_content() or ""
            self.page.keyboard.press("ArrowDown")
            try:
                expect(self._active_option).not_to_have_text(previous, timeout=SCAN_STEP_TIMEOUT_MS)
            except (AssertionError, PlaywrightTimeoutError):
                break  # the highlight did not move: end of the list
        raise AssertionError(f'Option not found in "{self.caption}"')
