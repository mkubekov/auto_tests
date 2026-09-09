from cmstest.http.client import ApiClient
from tests.unit.conftest import FakeSession


def test_url_joins_without_double_slashes(client: ApiClient) -> None:
    assert client.url("/content/things") == "https://api.example.com/api/v3/content/things"
    assert client.url("content/things") == "https://api.example.com/api/v3/content/things"


def test_api_key_header_is_added(client: ApiClient, fake_session: FakeSession) -> None:
    client.get("content/things")

    _, _, kwargs = fake_session.calls[-1]
    assert kwargs["headers"] == {"api-key": "test-key"}


def test_explicit_headers_win_over_defaults(client: ApiClient, fake_session: FakeSession) -> None:
    client.get("content/things", headers={"api-key": "other", "X-Trace": "1"})

    _, _, kwargs = fake_session.calls[-1]
    assert kwargs["headers"] == {"api-key": "other", "X-Trace": "1"}


def test_without_auth_shares_session_but_drops_credentials(
    client: ApiClient, fake_session: FakeSession
) -> None:
    anonymous = client.without_auth()
    anonymous.post("content/things", {"name": "x"})

    _, _, kwargs = fake_session.calls[-1]
    assert kwargs["headers"] == {}
    assert anonymous.base_url == client.base_url


def test_verbs_pass_json_params_and_timeout(client: ApiClient, fake_session: FakeSession) -> None:
    client.get("a", params={"q": 1})
    client.post("b", {"k": "v"})
    client.patch("c", {"k": "v"})
    client.put("d", {"k": "v"})
    client.delete("e")

    methods = [method for method, _, _ in fake_session.calls]
    assert methods == ["GET", "POST", "PATCH", "PUT", "DELETE"]
    assert fake_session.calls[0][2]["params"] == {"q": 1}
    assert fake_session.calls[1][2]["json"] == {"k": "v"}
    assert fake_session.calls[4][2]["json"] is None
    assert all(kwargs["timeout"] == client.timeout for _, _, kwargs in fake_session.calls)


def test_attach_false_still_sends(client: ApiClient, fake_session: FakeSession) -> None:
    client.post("content/things", {"name": "x"}, attach=False)

    assert len(fake_session.calls) == 1


def test_falsy_json_bodies_are_sent(client: ApiClient, fake_session: FakeSession) -> None:
    """Negative tests send ``False``, ``0`` and ``[]`` as bodies; they must not be dropped."""
    for body in (False, 0, [], {}):
        client.post("content/things", body)

    assert [kwargs["json"] for _, _, kwargs in fake_session.calls] == [False, 0, [], {}]
