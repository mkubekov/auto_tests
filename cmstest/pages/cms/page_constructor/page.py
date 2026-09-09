"""Page template form: SEO block, breadcrumbs and the list of composed blocks."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.http.references import references
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import DropDown, Indexing

# Reference collection that holds existing templates for each block type.
TEMPLATE_REFERENCES = {"textBlock": "text_blocks", "galleryBlock": "gallery_blocks"}


class Page(CmsPage):
    _is_active = '[id="isActive"]'
    _has_micro_markup = '[id="hasMicroMarkup"]'
    _add_breadcrumb = "Add breadcrumb"
    _add_block = "Add block"

    def __init__(self, page) -> None:
        super().__init__(page)
        self.indexing = Indexing(self)

    @staticmethod
    def _breadcrumb(index: int, field: str) -> str:
        return f'[id="breadcrumbs_{index}_{field}"]'

    @staticmethod
    def _block(index: int, field: str) -> str:
        return f'[id="blocks_{index}_{field}"]'

    def add_breadcrumb(self, index: int, crumb: dict[str, Any]) -> Self:
        with allure.step(f"Breadcrumb {index + 1}"):
            self.click_dashed(self._add_breadcrumb)
            self.fill("Breadcrumb text", self._breadcrumb(index, "name"), crumb["name"])
            self.fill("Breadcrumb path", self._breadcrumb(index, "path"), crumb["path"])
        return self

    def add_block(self, index: int, block: dict[str, Any]) -> Self:
        with allure.step(f"Block {index + 1}"):
            self.click_dashed(self._add_block)
            DropDown(self.page, "Block type", self._block(index, "blockType")).set(
                labels.BLOCK_TYPE[block["blockType"]]
            )
            template_name = references().value(TEMPLATE_REFERENCES[block["blockType"]], "name")
            DropDown(self.page, "Block template", self._block(index, "blockTemplateId")).select(
                template_name
            )
            self.fill("Scroll id", self._block(index, "scrollId"), block["scrollId"])
            self.check("Block fill", self._block(index, "blockFill"), block["blockFill"])
        return self

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create page template"):
            self.fill_name(payload["name"])
            self.switch("Active", self._is_active, payload["isActive"])
            self.fill("URL", self._url, payload["url"])
            self.switch("Micro markup", self._has_micro_markup, payload["hasMicroMarkup"])
            self.indexing.fill(payload)
            for index, crumb in enumerate(payload["breadcrumbs"]):
                self.add_breadcrumb(index, crumb)
            for index, block in enumerate(payload["blocks"]):
                self.add_block(index, block)
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_item("Active", payload["isActive"], created["isActive"])
        self.check_item("URL", payload["url"], created["url"])
        self.indexing.check(payload, created)
        self.check_item("Number of blocks", len(payload["blocks"]), len(created["blocks"]))
        for index, block in enumerate(payload["blocks"]):
            with allure.step(f"Block {index + 1}"):
                got = created["blocks"][index]
                self.check_item("Block type", block["blockType"], got["blockType"])
                self.check_item("Scroll id", block["scrollId"], got["scrollId"])
        return self
