"""Header needs an existing category, so it gets a dedicated flow instead of the generic one."""

from __future__ import annotations

import allure

from cmstest.data.enums import HttpStatus
from cmstest.http.assertions import assert_response
from cmstest.http.cleanup import CleanupStack
from cmstest.http.client import ApiClient
from cmstest.models import build_payload
from cmstest.registry import spec
from tests.e2e.helpers import create_entity

pytestmark = [allure.epic("Content API"), allure.suite("API"), allure.feature("CRUD")]


@allure.title("Header with a freshly created category can be created and updated")
def test_header_with_category(api_client: ApiClient, cleanup: CleanupStack) -> None:
    category, header = spec("headerCategories"), spec("headers")
    # Registered in this order, deleted in reverse: the header goes before its category.
    _, created_category = create_entity(api_client, cleanup, category)

    payload = build_payload(header.request_model)
    payload["categories"] = [created_category]
    _, created_header = create_entity(api_client, cleanup, header, payload)

    payload["name"] = f"{payload['name']}-patched"
    response = api_client.patch(f"{header.api_path}/{created_header['id']}", payload)
    assert_response(response, HttpStatus.OK, header.request_model)
