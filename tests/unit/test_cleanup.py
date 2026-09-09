from cmstest.http.cleanup import CleanupStack
from cmstest.http.client import ApiClient
from tests.unit.conftest import FakeSession, make_response


def _stack(*responses) -> tuple[CleanupStack, FakeSession]:
    session = FakeSession(*responses)
    client = ApiClient("https://api.example.com/api/v3", api_key="k", session=session)
    return CleanupStack(client), session


def test_deletes_in_reverse_order() -> None:
    stack, session = _stack(make_response(204), make_response(204))
    stack.add("content/header-categories/1")
    stack.add("content/headers/2")

    failed = stack.run()

    assert failed == []
    assert [url for _, url, _ in session.calls] == [
        "https://api.example.com/api/v3/content/headers/2",
        "https://api.example.com/api/v3/content/header-categories/1",
    ]
    assert stack.pending == ()


def test_failures_are_collected_and_do_not_stop_the_sweep() -> None:
    stack, session = _stack(make_response(500), make_response(404), make_response(204))
    for path in ("a/1", "a/2", "a/3"):
        stack.add(path)

    failed = stack.run()

    assert failed == ["a/3"]  # 500 for the first deleted (last added); 404 counts as gone
    assert len(session.calls) == 3


def test_exceptions_are_swallowed() -> None:
    class ExplodingSession(FakeSession):
        def request(self, method, url, *args, **kwargs):  # type: ignore[override]
            raise ConnectionError("stand is down")

    client = ApiClient("https://api.example.com", session=ExplodingSession())
    stack = CleanupStack(client)
    stack.add("a/1")

    assert stack.run() == ["a/1"]
