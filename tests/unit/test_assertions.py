import pytest
from pydantic import BaseModel

from cmstest.http.assertions import (
    assert_echo,
    assert_response,
    assert_schema,
    assert_status,
    json_value,
    response_json,
)
from tests.unit.conftest import make_response


class Thing(BaseModel):
    id: str
    name: str


def test_assert_status_message_names_request_and_body() -> None:
    response = make_response(500, {"error": "boom"}, method="POST")

    with pytest.raises(AssertionError) as excinfo:
        assert_status(response, 201)

    message = str(excinfo.value)
    assert "POST" in message
    assert "content/things" in message
    assert "500" in message
    assert "expected 201" in message
    assert "boom" in message


def test_response_json_quotes_non_json_body() -> None:
    response = make_response(200, text="<html>oops</html>")

    with pytest.raises(AssertionError, match="oops"):
        response_json(response)


def test_assert_schema_accepts_object_and_list() -> None:
    assert_schema(make_response(200, {"id": "1", "name": "a"}), Thing)
    assert_schema(make_response(200, [{"id": "1", "name": "a"}, {"id": "2", "name": "b"}]), Thing)


def test_assert_schema_reports_missing_fields() -> None:
    with pytest.raises(ValueError, match="name"):
        assert_schema(make_response(200, [{"id": "1"}]), Thing)


def test_assert_response_accepts_empty_204() -> None:
    assert_response(make_response(204), 204)


def test_assert_response_validates_schema() -> None:
    assert_response(make_response(201, {"id": "1", "name": "a"}), 201, Thing)

    with pytest.raises(ValueError, match="name"):
        assert_response(make_response(201, {"id": "1"}), 201, Thing)


def test_json_value_reports_missing_key() -> None:
    assert json_value(make_response(201, {"id": "42"}), "id") == "42"

    with pytest.raises(AssertionError, match="'id'"):
        json_value(make_response(201, {"name": "x"}), "id")


def test_assert_echo_flags_dropped_fields() -> None:
    sent = {"name": "n", "title": "t", "items": []}

    assert_echo({"id": "1", "name": "n", "title": "<p>t</p>", "items": []}, sent)

    with pytest.raises(AssertionError, match=r"\['items'\]"):
        assert_echo({"id": "1", "name": "n", "title": "t"}, sent)

    assert_echo({"id": "1", "name": "n", "title": "t"}, sent, ignore=["items"])
