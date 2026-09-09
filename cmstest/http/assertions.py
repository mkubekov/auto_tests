"""Assertions on HTTP responses. Every failure message says what was sent and what came back."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from typing import Any

import allure
from pydantic import BaseModel
from requests import Response

from cmstest.reporting.attachments import Attachments


def response_json(response: Response) -> Any:
    """Parsed body, or an AssertionError that quotes the raw text."""
    try:
        return response.json()
    except json.JSONDecodeError as err:
        raise AssertionError(f"Response is not JSON. Body: {response.text[:500]!r}") from err


def assert_status(response: Response, expected: int) -> None:
    assert response.status_code == int(expected), (
        f"{response.request.method} {response.url} returned {response.status_code}, "
        f"expected {int(expected)}. Body: {response.text[:500]!r}"
    )


def assert_schema(response: Response, model: type[BaseModel]) -> None:
    """Validate a dict body, or every item of a list body, against a pydantic model."""
    body = response_json(response)
    items = body if isinstance(body, list) else [body]
    for item in items:
        model.model_validate(item)


def assert_response(response: Response, status: int, schema: type[BaseModel] | None = None) -> None:
    """Attach curl/headers/body, check the status and optionally the schema.

    204 and empty bodies are accepted as-is; a non-empty body must be JSON.
    """
    title = f"Expect {int(status)}" + (f" and a valid {schema.__name__}" if schema else "")
    with allure.step(title):
        Attachments.curl(response)
        Attachments.headers(response)
        Attachments.response(response)
        assert_status(response, status)
        if int(status) == 204 or not response.text:
            return
        if schema is not None:
            assert_schema(response, schema)
        else:
            response_json(response)


def json_value(response: Response, key: str) -> Any:
    body = response_json(response)
    assert isinstance(body, Mapping), f"Expected a JSON object, got {type(body).__name__}"
    assert key in body, f"Key {key!r} is missing in the response: {response.text[:500]}"
    return body[key]


def assert_echo(
    created: Mapping[str, Any], sent: Mapping[str, Any], *, ignore: Iterable[str] = ()
) -> None:
    """Every key that was sent must be present in what the API returned.

    Values are not compared: servers normalise rich text, dates and file paths. A missing key,
    however, means the field was silently dropped, which a schema of optional fields cannot catch.
    """
    skipped = set(ignore)
    missing = [key for key in sent if key not in skipped and key not in created]
    assert not missing, f"Fields sent but absent in the response: {missing}"
