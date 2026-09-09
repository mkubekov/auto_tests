"""Rendered page composed from blocks on the public site."""

from __future__ import annotations

from typing import Any, Self

from cmstest.pages.site.base import SitePage


class Page(SitePage):
    # Locators are project-specific placeholders; point them at your front-end markup.
    _breadcrumbs = "nav.breadcrumbs"
    _block = "[data-block-type]"

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        for crumb in created["breadcrumbs"]:
            self.expect_text(
                "Breadcrumb", f'{self._breadcrumbs} a[href="{crumb["path"]}"]', crumb["name"]
            )
        for block in created["blocks"]:
            self.expect_visible(
                f"Block {block['blockType']}",
                f'{self._block}[data-block-type="{block["blockType"]}"]',
            )
        return self
