"""Rendered text block on the public site."""

from __future__ import annotations

from typing import Any, Self

from cmstest.pages.site.base import SitePage


class TextBlock(SitePage):
    # Locators are project-specific placeholders; point them at your front-end markup.
    _root = '[data-block-type="textBlock"]'

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.expect_visible("Text block", self._root)
        self.expect_text("Text", self._root, created["text"])
        return self
