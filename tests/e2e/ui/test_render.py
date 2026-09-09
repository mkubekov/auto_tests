"""Blocks created through the API must render on the public page that embeds them.

Skipped unless ``SITE_BASE_URL`` is configured: the site page objects are a scaffold whose
locators depend on the project's front-end.
"""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from cmstest.registry import page_block_params
from cmstest.settings import Settings

pytestmark = [allure.epic("Public site"), allure.suite("UI")]


@allure.title("{page_with_block} renders on the public page")
@pytest.mark.parametrize("page_with_block", page_block_params(), indirect=True)
def test_block_renders_on_public_page(
    site_page: Page, page_with_block: tuple, settings: Settings
) -> None:
    block, payload, created = page_with_block
    assert block.site_page is not None
    view = block.site_page(site_page)

    view.open(f"{settings.site_url}{settings.test_page_path}")
    view.check_created_item(payload, created)
