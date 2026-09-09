"""Small helpers shared by e2e tests."""

from __future__ import annotations

from typing import Any

import allure

from cmstest.data.enums import HttpStatus
from cmstest.http.assertions import assert_response
from cmstest.http.cleanup import CleanupStack
from cmstest.http.client import ApiClient
from cmstest.models.common import build_payload
from cmstest.registry import ModuleSpec


def create_entity(
    client: ApiClient,
    cleanup: CleanupStack,
    module: ModuleSpec,
    payload: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """POST a payload for ``module`` and return ``(payload, created)``.

    The entity is registered for cleanup *before* the assertion: if the assertion fails,
    teardown still deletes it and the original error message is what the report shows.
    """
    payload = payload if payload is not None else build_payload(module.request_model)
    with allure.step(f"Create {module.key}"):
        response = client.post(module.api_path, payload)
        if response.status_code == HttpStatus.CREATED:
            body = response.json()
            if isinstance(body, dict) and "id" in body:
                cleanup.add(f"{module.api_path}/{body['id']}")
        assert_response(response, HttpStatus.CREATED, module.request_model)
    return payload, response.json()
