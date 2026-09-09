import pytest
from pydantic import ValidationError

from cmstest.settings import Settings
from tests.unit.conftest import REQUIRED_SETTINGS, make_settings

ENV_NAMES = [name.upper() for name in Settings.model_fields]


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ENV_NAMES:
        monkeypatch.delenv(name, raising=False)


def test_defaults_derive_urls() -> None:
    settings = make_settings()

    assert settings.api_url == "https://api.example.com/api/v3"
    assert settings.cms_url == "https://cms.example.com"
    assert settings.cms_api_url == "https://cms.example.com/api/v1"
    assert settings.site_url is None
    assert settings.viewport_size == (1920, 1080)
    assert settings.request_timeout == (10, 60)


def test_explicit_urls_lose_trailing_slash() -> None:
    settings = make_settings(
        cms_api_base_url="https://auth.example.com/v1/", site_base_url="https://www.example.com/"
    )

    assert settings.cms_api_url == "https://auth.example.com/v1"
    assert settings.site_url == "https://www.example.com"


def test_viewport_is_parsed() -> None:
    assert make_settings(viewport="800x600").viewport_size == (800, 600)


@pytest.mark.parametrize("bad", ["1920", "1920 x 1080", "wide", "1920x"])
def test_viewport_rejects_garbage(bad: str) -> None:
    with pytest.raises(ValidationError, match="VIEWPORT"):
        make_settings(viewport=bad)


@pytest.mark.usefixtures("clean_env")
def test_missing_required_variables_are_named() -> None:
    with pytest.raises(ValidationError) as excinfo:
        Settings(_env_file=None)

    message = str(excinfo.value)
    for name in ("api_base_url", "cms_base_url", "api_key", "cms_email", "cms_password"):
        assert name in message


@pytest.mark.usefixtures("clean_env")
def test_environment_variables_are_read(monkeypatch: pytest.MonkeyPatch) -> None:
    for name, value in REQUIRED_SETTINGS.items():
        monkeypatch.setenv(name.upper(), value)
    monkeypatch.setenv("VIEWPORT", "1280x720")
    monkeypatch.setenv("REMOTE_BROWSER_WS", "ws://grid.example.com/playwright")

    settings = Settings(_env_file=None)

    assert settings.viewport_size == (1280, 720)
    assert settings.remote_browser_ws == "ws://grid.example.com/playwright"
    assert settings.api_key.get_secret_value() == "test-key"


def test_secrets_are_not_leaked_by_repr() -> None:
    settings = make_settings(api_key="very-secret", cms_password="also-secret")

    dump = repr(settings)
    assert "very-secret" not in dump
    assert "also-secret" not in dump
