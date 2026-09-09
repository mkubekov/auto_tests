"""SEO block shared by page-like entities: index flag plus meta title/description."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from cmstest.pages.cms.base import CmsPage


class Indexing:
    _is_indexed = '[id="isIndexed"]'
    _meta_title = '[id="metaTitle"]'
    _meta_description = '[id="metaDescription"]'

    def __init__(self, form: CmsPage) -> None:
        self.form = form

    def fill(self, payload: dict[str, Any]) -> Self:
        """``noIndex`` in the API is the inverse of the "Index this page" switch."""
        indexed = not payload.get("noIndex", False)
        self.form.switch("Index this page", self._is_indexed, indexed)
        if indexed:
            self.form.fill("Meta title", self._meta_title, payload["metaTitle"])
            self.form.fill("Meta description", self._meta_description, payload["metaDescription"])
        return self

    def check(self, sent: dict[str, Any], received: dict[str, Any]) -> Self:
        self.form.check_item("noIndex", sent.get("noIndex", False), received.get("noIndex", False))
        if not sent.get("noIndex", False):
            self.form.check_item("Meta title", sent["metaTitle"], received["metaTitle"])
            self.form.check_item(
                "Meta description", sent["metaDescription"], received["metaDescription"]
            )
        return self
