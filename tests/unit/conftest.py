"""Shared fakes for unit tests. No network, no browser, no ``.env``."""

from __future__ import annotations

import json
from typing import Any, ClassVar

import pytest
from requests import PreparedRequest, Request, Response, Session

from cmstest.http.client import ApiClient
from cmstest.http.references import ReferenceData, override_references
from cmstest.settings import Settings

REQUIRED_SETTINGS: dict[str, Any] = {
    "api_base_url": "https://api.example.com/api/v3",
    "cms_base_url": "https://cms.example.com",
    "api_key": "test-key",
    "cms_email": "qa@example.com",
    "cms_password": "test-password",
}


def make_settings(**overrides: Any) -> Settings:
    """Settings built from keyword arguments only: a developer's ``.env`` must not leak in."""
    return Settings(_env_file=None, **{**REQUIRED_SETTINGS, **overrides})


def make_response(
    status: int = 200,
    body: Any = None,
    *,
    text: str | None = None,
    method: str = "GET",
    url: str = "https://api.example.com/api/v3/content/things",
) -> Response:
    response = Response()
    response.status_code = status
    if text is not None:
        response._content = text.encode("utf8")
    elif body is not None:
        response._content = json.dumps(body).encode("utf8")
        response.headers["Content-Type"] = "application/json"
    else:
        response._content = b""
    response.url = url
    response.request = Request(method, url).prepare()
    return response


class FakeSession(Session):
    """Records calls and answers with scripted responses instead of touching the network."""

    def __init__(self, *responses: Response) -> None:
        super().__init__()
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self._responses = list(responses)

    def request(self, method: str, url: str, *args: Any, **kwargs: Any) -> Response:  # type: ignore[override]
        self.calls.append((method, url, kwargs))
        if self._responses:
            return self._responses.pop(0)
        return make_response(200, {}, method=method, url=url)

    @property
    def last_request(self) -> PreparedRequest:
        method, url, _ = self.calls[-1]
        return Request(method, url).prepare()


class StubReferences(ReferenceData):
    """Answers every reference lookup with the same synthetic entity."""

    ENTITY: ClassVar[dict[str, Any]] = {
        "id": "00000000-0000-4000-8000-000000000001",
        "name": "stub",
        "value": "/stub",
        "city": "Stubtown",
    }

    def __init__(self) -> None:
        super().__init__(client=ApiClient("https://stub.invalid", session=FakeSession()))

    def first(self, key: str) -> dict[str, Any]:
        return dict(self.ENTITY)


@pytest.fixture
def fake_session() -> FakeSession:
    return FakeSession()


@pytest.fixture
def client(fake_session: FakeSession) -> ApiClient:
    return ApiClient("https://api.example.com/api/v3/", api_key="test-key", session=fake_session)


@pytest.fixture
def stub_references():
    with override_references(StubReferences()):
        yield
