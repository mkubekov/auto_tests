"""Single source of configuration: environment variables plus an optional ``.env`` file.

Everything that depends on a concrete stand lives here. Nothing in ``cmstest`` reads
``os.environ`` directly except the Faker locale (see ``cmstest.data.generators``), so
importing models or page objects never requires a configured environment.
"""

from __future__ import annotations

import re
from functools import lru_cache

from pydantic import Field, HttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_VIEWPORT_RE = re.compile(r"^(\d{3,5})x(\d{3,5})$")


def _strip_slash(url: HttpUrl) -> str:
    return str(url).rstrip("/")


class Settings(BaseSettings):
    """Stand-specific settings. Field names double as environment variable names."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    api_base_url: HttpUrl = Field(
        description="Content API root, e.g. https://api.example.com/api/v3"
    )
    cms_base_url: HttpUrl = Field(description="Admin panel root, e.g. https://cms.example.com")
    cms_api_base_url: HttpUrl | None = Field(
        default=None, description="Admin auth API root; defaults to <cms_base_url>/api/v1"
    )
    site_base_url: HttpUrl | None = Field(
        default=None, description="Public site root; UI tests are skipped when unset"
    )

    api_key: SecretStr = Field(description="Value of the api-key header")
    cms_email: str = Field(description="Admin panel login")
    cms_password: SecretStr = Field(description="Admin panel password")

    test_page_path: str = Field(default="/autotest", description="Public page used by UI tests")
    viewport: str = Field(default="1920x1080", description="Browser viewport as WIDTHxHEIGHT")
    remote_browser_ws: str | None = Field(
        default=None,
        description="ws:// endpoint of a remote Playwright server or grid; empty = local browser",
    )
    browser_timeout_ms: int = Field(default=240_000, ge=1_000)
    connect_timeout_s: float = Field(default=10, gt=0)
    read_timeout_s: float = Field(default=60, gt=0)
    faker_seed: int | None = Field(default=None, description="Fixed seed to replay a run")
    global_search_path: str | None = Field(
        default="content/global-search",
        description="Endpoint that finds entities by name across modules; empty disables the sweep",
    )

    @field_validator("viewport")
    @classmethod
    def _check_viewport(cls, value: str) -> str:
        if not _VIEWPORT_RE.match(value):
            raise ValueError(f"VIEWPORT must look like 1920x1080, got {value!r}")
        return value

    @property
    def viewport_size(self) -> tuple[int, int]:
        """``"1920x1080"`` -> ``(1920, 1080)``."""
        match = _VIEWPORT_RE.match(self.viewport)
        assert match is not None  # guaranteed by the validator
        return int(match.group(1)), int(match.group(2))

    @property
    def api_url(self) -> str:
        return _strip_slash(self.api_base_url)

    @property
    def cms_url(self) -> str:
        return _strip_slash(self.cms_base_url)

    @property
    def cms_api_url(self) -> str:
        if self.cms_api_base_url is not None:
            return _strip_slash(self.cms_api_base_url)
        return f"{self.cms_url}/api/v1"

    @property
    def site_url(self) -> str | None:
        return _strip_slash(self.site_base_url) if self.site_base_url else None

    @property
    def request_timeout(self) -> tuple[float, float]:
        """``(connect, read)`` timeout for HTTP calls. Without it a hung stand hangs the CI job."""
        return self.connect_timeout_s, self.read_timeout_s


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings instance. Missing required variables raise a descriptive error."""
    return Settings()
