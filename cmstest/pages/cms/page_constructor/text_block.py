"""Text block form."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import TextEditor


class TextBlock(CmsPage):
    _text = '[id="text"]'

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create text block"):
            self.fill_name(payload["name"])
            TextEditor(self.page, "Text", self._text).type(payload["text"])
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_text("Text", payload["text"], created["text"])
        return self
