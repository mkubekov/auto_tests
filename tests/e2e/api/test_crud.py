"""Positive API checks for every registered module."""

from __future__ import annotations

import allure
import pytest

from cmstest.data.enums import HttpStatus
from cmstest.http.assertions import assert_echo, assert_response, json_value
from cmstest.http.cleanup import CleanupStack
from cmstest.http.client import ApiClient
from cmstest.registry import api_params, spec, writable_params
from tests.e2e.helpers import create_entity

pytestmark = [allure.epic("Content API"), allure.suite("API"), allure.feature("CRUD")]


@allure.title("GET {module_key}: the collection is readable and matches the schema")
@pytest.mark.parametrize("module_key", api_params())
def test_list(module_key: str, api_client: ApiClient) -> None:
    module = spec(module_key)

    response = api_client.get(module.api_path)

    assert_response(response, HttpStatus.OK, module.request_model)


@allure.title("POST {module_key}: the entity is created with every field sent")
@pytest.mark.parametrize("module_key", writable_params())
def test_create(module_key: str, api_client: ApiClient, cleanup: CleanupStack) -> None:
    module = spec(module_key)

    payload, created = create_entity(api_client, cleanup, module)

    assert_echo(created, payload)


@allure.title("PATCH {module_key}: the change is persisted")
@pytest.mark.parametrize("module_key", writable_params())
def test_update(module_key: str, api_client: ApiClient, cleanup: CleanupStack) -> None:
    module = spec(module_key)
    payload, created = create_entity(api_client, cleanup, module)
    item_path = f"{module.api_path}/{created['id']}"
    payload[module.patch_field] = f"{payload[module.patch_field]}-patched"

    response = api_client.patch(item_path, payload)
    assert_response(response, HttpStatus.OK, module.request_model)

    with allure.step("Read the entity back"):
        stored = api_client.get(item_path)
        assert_response(stored, HttpStatus.OK, module.request_model)
        assert json_value(stored, module.patch_field) == payload[module.patch_field]


@allure.title("DELETE {module_key}: the entity disappears")
@pytest.mark.parametrize("module_key", writable_params())
def test_delete(module_key: str, api_client: ApiClient, cleanup: CleanupStack) -> None:
    module = spec(module_key)
    _, created = create_entity(api_client, cleanup, module)
    item_path = f"{module.api_path}/{created['id']}"

    assert_response(api_client.delete(item_path), HttpStatus.NO_CONTENT)
    assert_response(api_client.get(item_path), HttpStatus.NOT_FOUND)
