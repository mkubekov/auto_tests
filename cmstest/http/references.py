"""Reference entities that request models depend on (categories, cities, footer sections...).

Models call ``references().value("categories", "value")`` inside ``default_factory``, i.e. at
instantiation time. The active :class:`ReferenceData` is a module-level singleton set by the
test session; unit tests swap it for a stub with :func:`override_references`.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any

from cmstest.http.client import ApiClient

# Where each reference collection lives. Query strings are allowed.
DEFAULT_REFERENCE_PATHS: dict[str, str] = {
    "categories": "content/handbooks?type=categories",
    "labels": "content/handbooks?type=labels",
    "cities": "content/cities",
    "footer_sections": "content/footer-sections",
    "header_categories": "content/header-categories",
    "header_subcategories": "content/header-subcategories",
}


class ReferenceData:
    """Fetches the first item of each reference collection once and caches it.

    Errors are not swallowed: an empty dictionary silently turned into a default value
    produces an obscure 400 much later, far from the cause.
    """

    def __init__(
        self, client: ApiClient, paths: Mapping[str, str] = DEFAULT_REFERENCE_PATHS
    ) -> None:
        self._client = client
        self._paths = dict(paths)
        self._cache: dict[str, dict[str, Any]] = {}

    def first(self, key: str) -> dict[str, Any]:
        if key in self._cache:
            return self._cache[key]
        if key not in self._paths:
            raise KeyError(f"Unknown reference {key!r}; known: {sorted(self._paths)}")

        path = self._paths[key]
        response = self._client.get(path, attach=False)
        if response.status_code != 200:
            raise RuntimeError(
                f"Reference {key!r}: {response.status_code} from {path}: {response.text[:200]}"
            )
        payload = response.json()
        if isinstance(payload, list):
            if not payload:
                raise RuntimeError(f"Reference {key!r} is empty: nothing to use as a default")
            payload = payload[0]
        if not isinstance(payload, dict):
            raise RuntimeError(f"Reference {key!r}: unexpected payload {type(payload).__name__}")
        self._cache[key] = payload
        return payload

    def value(self, key: str, field: str) -> Any:
        return self.first(key)[field]

    def clear(self) -> None:
        self._cache.clear()


_current: ReferenceData | None = None


def references() -> ReferenceData:
    if _current is None:
        raise RuntimeError(
            "Reference data is not configured. Call set_references() in a session fixture "
            "or wrap the code in override_references() in unit tests."
        )
    return _current


def set_references(data: ReferenceData | None) -> None:
    global _current  # deliberate process-wide singleton
    _current = data


@contextmanager
def override_references(data: ReferenceData) -> Iterator[None]:
    previous = _current
    set_references(data)
    try:
        yield
    finally:
        set_references(previous)
