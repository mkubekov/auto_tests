"""Negative API checks: authentication, validation, idempotency and routing errors.

Every error response must carry the :class:`ErrorResponse` envelope; a bare status code
without a body is a defect too.
"""

from __future__ import annotations

import allure
import pytest

from cmstest.data.enums import HttpStatus
from cmstest.http.assertions import assert_response
from cmstest.http.cleanup import CleanupStack
from cmstest.http.client import ApiClient
from cmstest.models import ErrorResponse, build_payload
from cmstest.registry import spec, writable_params
from tests.e2e.helpers import create_entity

pytestmark = [allure.epic("Content API"), allure.suite("API"), allure.feature("Negative")]

MALFORMED_BODIES = [
    pytest.param({}, id="empty-object"),
    pytest.param([], id="empty-list"),
    pytest.param(333, id="number"),
    pytest.param("text", id="string"),
    pytest.param(False, id="boolean"),
]


@allure.title("POST {module_key} without an API key is forbidden")
@pytest.mark.parametrize("module_key", writable_params())
def test_create_without_api_key(module_key: str, anon_client: ApiClient) -> None:
    module = spec(module_key)

    response = anon_client.post(module.api_path, build_payload(module.request_model))

    assert_response(response, HttpStatus.FORBIDDEN, ErrorResponse)


@allure.title("POST {module_key} with a malformed body ({body}) is rejected")
@pytest.mark.parametrize("body", MALFORMED_BODIES)
@pytest.mark.parametrize("module_key", writable_params())
def test_malformed_body(module_key: str, body: object, api_client: ApiClient) -> None:
    module = spec(module_key)

    response = api_client.post(module.api_path, body)

    assert_response(response, HttpStatus.BAD_REQUEST, ErrorResponse)


@allure.title("POST {module_key} twice with the same payload conflicts")
@pytest.mark.parametrize("module_key", writable_params())
def test_duplicate_create(module_key: str, api_client: ApiClient, cleanup: CleanupStack) -> None:
    module = spec(module_key)
    payload, _ = create_entity(api_client, cleanup, module)

    response = api_client.post(module.api_path, payload)

    assert_response(response, HttpStatus.CONFLICT, ErrorResponse)


@allure.title("POST {module_key}/<id> is not a valid route")
@pytest.mark.parametrize("module_key", writable_params())
def test_post_to_item_url(module_key: str, api_client: ApiClient, cleanup: CleanupStack) -> None:
    module = spec(module_key)
    payload, created = create_entity(api_client, cleanup, module)

    response = api_client.post(f"{module.api_path}/{created['id']}", payload)

    assert_response(response, HttpStatus.NOT_FOUND, ErrorResponse)


@allure.title("DELETE {module_key}/<id> twice: second call is not found")
@pytest.mark.parametrize("module_key", writable_params())
def test_double_delete(module_key: str, api_client: ApiClient, cleanup: CleanupStack) -> None:
    module = spec(module_key)
    _, created = create_entity(api_client, cleanup, module)
    item_path = f"{module.api_path}/{created['id']}"

    assert_response(api_client.delete(item_path), HttpStatus.NO_CONTENT)
    assert_response(api_client.delete(item_path), HttpStatus.NOT_FOUND, ErrorResponse)


@allure.title("PUT {module_key} is not supported")
@pytest.mark.parametrize("module_key", writable_params())
def test_unsupported_method(module_key: str, api_client: ApiClient) -> None:
    module = spec(module_key)

    response = api_client.put(module.api_path, {})

    # This API answers 404, not 405, for verbs it does not route. Encoded on purpose.
    assert_response(response, HttpStatus.NOT_FOUND, ErrorResponse)


@allure.title("Unknown resource returns 404 for every verb")
def test_unknown_resource(api_client: ApiClient) -> None:
    path = "content/does-not-exist"

    for send in (
        lambda: api_client.post(path, {}),
        lambda: api_client.get(path),
        lambda: api_client.patch(path, {}),
        lambda: api_client.delete(path),
    ):
        assert_response(send(), HttpStatus.NOT_FOUND, ErrorResponse)
