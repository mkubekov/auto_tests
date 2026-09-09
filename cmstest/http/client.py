"""Thin HTTP client on top of ``requests.Session`` with Allure logging."""

from __future__ import annotations

from typing import Any

import allure
from requests import Response, Session
from requests.adapters import HTTPAdapter

from cmstest.reporting.attachments import Attachments

DEFAULT_TIMEOUT: tuple[float, float] = (10.0, 60.0)
_METHODS_WITH_BODY = frozenset({"POST", "PATCH", "PUT"})


def build_session(pool_connections: int = 10, pool_maxsize: int = 20) -> Session:
    """Session with connection pooling: TCP/TLS handshakes are reused across requests."""
    session = Session()
    adapter = HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


class ApiClient:
    """HTTP client bound to one base URL and one API key.

    One instance per process is enough. Under pytest-xdist every worker is a separate
    process, so sharing the underlying session is safe.
    """

    def __init__(
        self,
        base_url: str,
        *,
        api_key: str | None = None,
        api_key_header: str = "api-key",
        timeout: tuple[float, float] = DEFAULT_TIMEOUT,
        session: Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._api_key = api_key
        self._api_key_header = api_key_header
        self._session = session or build_session()

    @property
    def default_headers(self) -> dict[str, str]:
        return {self._api_key_header: self._api_key} if self._api_key else {}

    def without_auth(self) -> ApiClient:
        """Same base URL and session, no credentials. Used by negative tests."""
        return ApiClient(
            self.base_url,
            api_key=None,
            api_key_header=self._api_key_header,
            timeout=self.timeout,
            session=self._session,
        )

    def url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        attach: bool = True,
    ) -> Response:
        """Send a request. ``attach=False`` keeps housekeeping calls out of the report."""
        method = method.upper()
        if attach:
            with allure.step(f"{method} {path}"):
                if json is not None and method in _METHODS_WITH_BODY:
                    Attachments.body(json, "Request body")
        return self._session.request(
            method,
            self.url(path),
            json=json,
            params=params,
            files=files,
            headers={**self.default_headers, **(headers or {})},
            cookies=cookies,
            timeout=self.timeout,
        )

    def get(self, path: str, *, params: dict[str, Any] | None = None, **kwargs: Any) -> Response:
        return self.request("GET", path, params=params, **kwargs)

    def post(self, path: str, json: Any = None, **kwargs: Any) -> Response:
        return self.request("POST", path, json=json, **kwargs)

    def patch(self, path: str, json: Any = None, **kwargs: Any) -> Response:
        return self.request("PATCH", path, json=json, **kwargs)

    def put(self, path: str, json: Any = None, **kwargs: Any) -> Response:
        return self.request("PUT", path, json=json, **kwargs)

    def delete(self, path: str, json: Any = None, **kwargs: Any) -> Response:
        return self.request("DELETE", path, json=json, **kwargs)
