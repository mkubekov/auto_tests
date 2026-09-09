"""Teardown helper: remembers what a test created and deletes it afterwards."""

from __future__ import annotations

import logging

from cmstest.http.client import ApiClient

log = logging.getLogger(__name__)


class CleanupStack:
    """Register entity paths as they are created; :meth:`run` deletes them in reverse order.

    Reverse order matters: a dependent entity (a header) must go before the entity it
    references (a header category). Failures are logged, never raised, so a cleanup problem
    cannot mask the assertion that failed the test.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client
        self._paths: list[str] = []

    def add(self, path: str) -> str:
        self._paths.append(path)
        return path

    @property
    def pending(self) -> tuple[str, ...]:
        return tuple(self._paths)

    def run(self) -> list[str]:
        """Delete everything registered. Returns the paths that could not be deleted."""
        failed: list[str] = []
        for path in reversed(self._paths):
            try:
                response = self._client.delete(path, attach=False)
            except Exception as err:  # noqa: BLE001 - teardown must not raise
                log.warning("cleanup: DELETE %s raised %r", path, err)
                failed.append(path)
                continue
            if response.status_code not in (200, 204, 404):
                log.warning("cleanup: DELETE %s returned %s", path, response.status_code)
                failed.append(path)
        self._paths.clear()
        return failed
