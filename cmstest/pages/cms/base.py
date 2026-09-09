"""Base page object for admin-panel forms (Ant Design)."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any, Self

import allure
from bs4 import BeautifulSoup
from playwright.sync_api import Page, Response

from cmstest.data import labels
from cmstest.data.files import resource_path
from cmstest.http.client import ApiClient


def strip_html(value: str) -> str:
    """Rich-text fields come back wrapped in tags (``<p>...</p>``); compare the text only."""
    return BeautifulSoup(value, "html.parser").get_text()


class CmsPage:
    """Fluent Playwright helpers for admin forms plus the contract every module implements.

    The admin panel renders inputs with ``id`` equal to the API field name, so locators are
    ``[id="..."]``. There are no test ids in the markup; that is a constraint of the target
    application, not a choice.

    Subclasses implement :meth:`create_element` and :meth:`check_created_item`.
    """

    # Locators shared by many forms.
    _name = '[id="name"]'
    _image = '[for="image"]'
    _title = '[id="title"]'
    _subtitle = '[id="subtitle"]'
    _link = '[id="link"]'
    _description = '[id="description"]'
    _priority = '[id="priority"]'
    _cities = '[id="cities"]'
    _categories = '[id="categories"]'
    _position = '[id="position"]'
    _category = '[id="category"]'
    _url = '[id="url"]'
    _actionType = '[id="actionType"]'
    _color = '[id="color"]'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.created_id: str | None = None

    # -- form primitives ---------------------------------------------------------------

    def fill(self, caption: str, locator: str, value: Any) -> Self:
        with allure.step(f'Fill "{caption}": {value}'):
            self.page.locator(locator).fill(str(value))
        return self

    def click(self, caption: str, locator: str) -> Self:
        with allure.step(f'Click "{caption}"'):
            self.page.locator(locator).click()
        return self

    def switch(self, caption: str, locator: str, active: bool) -> Self:
        """Toggle an Ant ``Switch`` so that its ``aria-checked`` matches ``active``."""
        with allure.step(f'Set switch "{caption}" to {active}'):
            element = self.page.locator(locator)
            is_on = element.get_attribute("aria-checked") == "true"
            if is_on != active:
                element.click()
        return self

    def check(self, caption: str, locator: str, active: bool) -> Self:
        """Toggle an Ant ``Checkbox``; the checked state lives on the wrapper's class list."""
        with allure.step(f'Set checkbox "{caption}" to {active}'):
            element = self.page.locator(locator)
            is_checked = element.locator("..").evaluate(
                '(node) => node.classList.contains("ant-checkbox-checked")'
            )
            if is_checked != active:
                element.click()
        return self

    def upload(self, caption: str, locator: str, file_name: str) -> Self:
        """Upload a fixture file through the uploader anchored at its caption label."""
        with allure.step(f'Upload "{caption}": {file_name}'):
            uploader = self.page.locator(locator).locator("../..")
            uploader.locator('[type="file"]').set_input_files([resource_path(file_name)])
            uploader.get_by_text(labels.DELETE).wait_for(state="visible")
        return self

    def click_dashed(self, caption: str) -> Self:
        """Click an "add item" button; Ant renders those as dashed buttons."""
        with allure.step(f'Click "{caption}"'):
            self.page.locator(".ant-btn-dashed").get_by_text(caption).last.click()
        return self

    def switch_tab(self, caption: str) -> Self:
        with allure.step(f'Open tab "{caption}"'):
            self.page.locator(".ant-tabs-tab").get_by_text(caption).first.click()
        return self

    def fill_name(self, value: str) -> Self:
        return self.fill(labels.SYSTEM_NAME, self._name, value)

    def save(self) -> Self:
        """Submit the form and remember the id of the created entity.

        The response listener is removed in ``finally``: otherwise it would stay attached to
        the page and overwrite ``created_id`` with every later 201.
        """
        with allure.step("Save"):
            self.page.on("response", self._capture_created_id)
            try:
                self.page.locator('[type="button"]').get_by_text(labels.SAVE).click()
                self.page.locator(labels.SUCCESS_LOCATOR).wait_for(state="visible")
            finally:
                self.page.remove_listener("response", self._capture_created_id)
        return self

    def cancel(self) -> Self:
        with allure.step("Cancel"):
            self.page.get_by_text(labels.CANCEL).click()
        return self

    def _capture_created_id(self, response: Response) -> None:
        if response.status != 201:
            return
        try:
            body = response.json()
        except ValueError:
            return
        if isinstance(body, dict) and "id" in body:
            self.created_id = body["id"]

    # -- assertions --------------------------------------------------------------------

    def check_item(self, caption: str, sent: Any, received: Any) -> Self:
        with allure.step(caption):
            assert sent == received, f"\nSent:     {sent!r}\nReceived: {received!r}"
        return self

    def check_text(self, caption: str, sent: str, received_html: str) -> Self:
        """Compare a rich-text field ignoring the markup the editor adds."""
        return self.check_item(caption, sent, strip_html(received_html))

    def check_file(self, caption: str, sent: str, received_path: str) -> Self:
        """Uploaded files come back as storage paths; only the file name is comparable."""
        return self.check_item(caption, Path(sent).name, Path(received_path).name)

    # -- contract ----------------------------------------------------------------------

    def create_element(self, payload: dict[str, Any]) -> Self:
        raise NotImplementedError

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        raise NotImplementedError

    def verify_created(
        self,
        client: ApiClient,
        api_path: str,
        payload: dict[str, Any],
        *,
        checks: Callable[[dict[str, Any], dict[str, Any]], Any] | None = None,
    ) -> dict[str, Any]:
        """Read the entity back through the API and run the field checks.

        Prefers ``GET {api_path}/{id}`` with the id captured on save; falls back to a lookup
        by name in the collection. Returns the entity so the caller can register cleanup.
        The entity is deliberately not deleted here: cleanup belongs to fixtures.
        """
        with allure.step("Verify the created entity through the API"):
            created = self._fetch_created(client, api_path, payload["name"])
            assert created is not None, f"Entity {payload['name']!r} was not found via API"
            (checks or self.check_created_item)(payload, created)
        return created

    def _fetch_created(self, client: ApiClient, api_path: str, name: str) -> dict[str, Any] | None:
        if self.created_id:
            response = client.get(f"{api_path}/{self.created_id}", attach=False)
            if response.status_code == 200:
                return response.json()
        response = client.get(api_path, attach=False)
        if response.status_code != 200:
            return None
        items = response.json()
        if not isinstance(items, list):
            return None
        return next((item for item in items if item.get("name") == name), None)
