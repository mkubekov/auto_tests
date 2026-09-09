import pytest

from cmstest.http.client import ApiClient
from cmstest.http.references import (
    ReferenceData,
    override_references,
    references,
    set_references,
)
from tests.unit.conftest import FakeSession, make_response

PATHS = {"categories": "content/handbooks?type=categories"}


def _data(*responses) -> tuple[ReferenceData, FakeSession]:
    session = FakeSession(*responses)
    client = ApiClient("https://api.example.com/api/v3", api_key="k", session=session)
    return ReferenceData(client, PATHS), session


def test_first_item_is_cached() -> None:
    data, session = _data(make_response(200, [{"id": "1", "value": "/a"}, {"id": "2"}]))

    assert data.value("categories", "value") == "/a"
    assert data.first("categories")["id"] == "1"
    assert len(session.calls) == 1


def test_object_payload_is_accepted_as_is() -> None:
    data, _ = _data(make_response(200, {"id": "solo"}))

    assert data.first("categories") == {"id": "solo"}


def test_unknown_key_is_rejected_before_any_request() -> None:
    data, session = _data()

    with pytest.raises(KeyError, match="unknown"):
        data.first("unknown")
    assert session.calls == []


def test_empty_collection_raises_instead_of_returning_nothing() -> None:
    data, _ = _data(make_response(200, []))

    with pytest.raises(RuntimeError, match="empty"):
        data.first("categories")


def test_error_status_is_reported_with_body() -> None:
    data, _ = _data(make_response(503, text="maintenance"))

    with pytest.raises(RuntimeError, match="503.*maintenance"):
        data.first("categories")


def test_singleton_requires_configuration() -> None:
    set_references(None)
    with pytest.raises(RuntimeError, match="not configured"):
        references()


def test_override_restores_previous_value() -> None:
    outer, _ = _data()
    inner, _ = _data()
    set_references(outer)
    try:
        with override_references(inner):
            assert references() is inner
        assert references() is outer
    finally:
        set_references(None)
