"""Rendered gallery block on the public site."""

from __future__ import annotations

from typing import Any, Self

from cmstest.pages.site.base import SitePage


class GalleryBlock(SitePage):
    # Locators are project-specific placeholders; point them at your front-end markup.
    _root = '[data-block-type="galleryBlock"]'
    _slide_title = f"{_root} .slide-title"
    _slide_text = f"{_root} .slide-text"
    _next_slide = f"{_root} .slide-next"

    def next_slide(self) -> Self:
        return self.click("Next slide", self._next_slide)

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.expect_visible("Gallery block", self._root)
        for index, slide in enumerate(created["galleryList"]):
            if index:
                self.next_slide()
            self.expect_text("Slide title", self._slide_title, slide["title"])
            self.expect_text("Slide text", self._slide_text, slide["text"])
        return self
