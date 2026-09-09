import json
import warnings

import pytest
from pydantic import ValidationError

from cmstest.data.generators import run_marker
from cmstest.models import ErrorResponse, HeaderSubcategory, build_payload
from cmstest.registry import MODULES


@pytest.mark.usefixtures("stub_references")
@pytest.mark.parametrize("module_key", list(MODULES), ids=list(MODULES))
def test_payload_is_json_serialisable_and_carries_the_run_marker(module_key: str) -> None:
    with warnings.catch_warnings():
        # A pydantic serializer warning means a field type and its generator disagree.
        warnings.simplefilter("error")
        payload = build_payload(MODULES[module_key].request_model)

    json.dumps(payload)
    assert payload["name"].startswith(run_marker())
    assert "id" not in payload, "server-managed fields must not be sent"


@pytest.mark.usefixtures("stub_references")
def test_each_call_generates_fresh_data() -> None:
    first = build_payload(MODULES["webhooks"].request_model)
    second = build_payload(MODULES["webhooks"].request_model)

    assert first["name"] != second["name"]


@pytest.mark.usefixtures("stub_references")
def test_reserved_json_keys_are_sent_under_their_alias() -> None:
    payload = build_payload(HeaderSubcategory)

    assert "list" in payload
    assert "items" not in payload


def test_error_response_rejects_an_empty_body() -> None:
    with pytest.raises(ValidationError):
        ErrorResponse.model_validate({})

    ErrorResponse.model_validate(
        {"statusCode": 400, "response": {"message": "x"}, "timestamp": "t", "path": "/p"}
    )
