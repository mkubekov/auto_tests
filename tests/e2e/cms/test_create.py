"""Create every module through the admin panel and verify the result via the API."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from cmstest.data import labels
from cmstest.http.cleanup import CleanupStack
from cmstest.http.client import ApiClient
from cmstest.models import build_payload
from cmstest.registry import cms_params, spec
from cmstest.settings import Settings

pytestmark = [allure.epic("Admin panel"), allure.suite("CMS")]


@allure.title("Create {module_key} through the admin form")
@pytest.mark.parametrize("module_key", cms_params())
def test_create_via_admin_panel(
    module_key: str,
    cms_page: Page,
    api_client: ApiClient,
    cleanup: CleanupStack,
    settings: Settings,
) -> None:
    module = spec(module_key)
    assert module.cms_page is not None
    assert module.cms_path is not None
    form = module.cms_page(cms_page)
    payload = build_payload(module.request_model)

    with allure.step(f"Open {module.cms_path} and start a new entity"):
        cms_page.goto(f"{settings.cms_url}/{module.cms_path}")
        cms_page.get_by_text(labels.ADD).click()

    form.create_element(payload)
    if form.created_id:
        cleanup.add(f"{module.api_path}/{form.created_id}")

    created = form.verify_created(api_client, module.api_path, payload)
    if not form.created_id:
        cleanup.add(f"{module.api_path}/{created['id']}")
