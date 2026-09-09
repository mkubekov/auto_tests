"""Fixtures that talk to a stand or drive a browser. Loaded for ``tests/e2e`` only."""

from __future__ import annotations

import contextlib
import logging
import os
import subprocess
from collections.abc import Generator, Iterator
from pathlib import Path
from typing import Any

import allure
import pytest
from playwright.sync_api import BrowserContext, Page

from cmstest.data.generators import run_marker
from cmstest.http.cleanup import CleanupStack
from cmstest.http.client import ApiClient
from cmstest.http.references import ReferenceData, set_references
from cmstest.models.common import build_payload
from cmstest.registry import MODULES, ModuleSpec, spec
from cmstest.reporting.attachments import Attachments
from cmstest.settings import Settings, get_settings
from tests.conftest import FAKER_SEED_KEY
from tests.e2e.helpers import create_entity

log = logging.getLogger(__name__)

AUTH_COOKIES = ("Authentication", "Refresh")

# -- configuration and HTTP ----------------------------------------------------------------


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def api_client(settings: Settings) -> Iterator[ApiClient]:
    client = ApiClient(
        settings.api_url,
        api_key=settings.api_key.get_secret_value(),
        timeout=settings.request_timeout,
    )
    # Request models resolve reference entities through this client.
    set_references(ReferenceData(client))
    yield client
    set_references(None)


@pytest.fixture(scope="session")
def anon_client(api_client: ApiClient) -> ApiClient:
    return api_client.without_auth()


@pytest.fixture
def cleanup(api_client: ApiClient) -> Iterator[CleanupStack]:
    stack = CleanupStack(api_client)
    yield stack
    failed = stack.run()
    if failed:
        log.warning("cleanup left %d entities behind: %s", len(failed), failed)


@pytest.fixture(scope="session", autouse=True)
def sweep_run_entities(api_client: ApiClient, settings: Settings) -> Iterator[None]:
    """Delete whatever still carries this run's marker when the session ends.

    The marker is unique per process, so parallel workers and other runs on a shared stand
    are never touched. Uses the global search endpoint when the stand offers one.
    """
    yield
    if not settings.global_search_path:
        return
    response = api_client.get(
        settings.global_search_path, params={"name": run_marker()}, attach=False
    )
    if response.status_code != 200 or not isinstance(response.json(), dict):
        return
    for module_key, items in response.json().items():
        module = MODULES.get(module_key)
        if module is None:
            continue
        for item in items:
            with contextlib.suppress(Exception):
                api_client.delete(f"{module.api_path}/{item['id']}", attach=False)


# -- admin panel authentication ------------------------------------------------------------


@pytest.fixture(scope="session")
def cms_cookies(settings: Settings) -> Iterator[dict[str, str]]:
    """Log in through the admin API once per session; the browser reuses the cookies."""
    auth_client = ApiClient(settings.cms_api_url, timeout=settings.request_timeout)
    response = auth_client.post(
        "auth/login",
        {"email": settings.cms_email, "password": settings.cms_password.get_secret_value()},
        attach=False,
    )
    assert response.status_code == 200, (
        f"CMS login failed: {response.status_code} {response.text[:200]}"
    )
    assert AUTH_COOKIES[0] in response.cookies, "Login response has no Authentication cookie"
    cookies: dict[str, str] = {
        name: str(response.cookies[name]) for name in AUTH_COOKIES if name in response.cookies
    }
    yield cookies
    auth_client.post(
        "auth/logout", cookies={AUTH_COOKIES[0]: cookies[AUTH_COOKIES[0]]}, attach=False
    )


# -- browser (overrides of pytest-playwright fixtures) -------------------------------------


@pytest.fixture(scope="session")
def connect_options(settings: Settings) -> dict[str, Any] | None:
    """Remote Playwright server or grid when ``REMOTE_BROWSER_WS`` is set, local otherwise."""
    if not settings.remote_browser_ws:
        return None
    return {"ws_endpoint": settings.remote_browser_ws, "timeout": settings.browser_timeout_ms}


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict, settings: Settings) -> dict:
    return {**browser_type_launch_args, "timeout": settings.browser_timeout_ms}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, settings: Settings) -> dict:
    width, height = settings.viewport_size
    return {**browser_context_args, "viewport": {"width": width, "height": height}}


@pytest.fixture
def cms_page(context: BrowserContext, cms_cookies: dict[str, str], settings: Settings) -> Page:
    """A page already authenticated in the admin panel."""
    context.add_cookies(
        [
            {"name": name, "value": value, "url": settings.cms_url}
            for name, value in cms_cookies.items()
        ]
    )
    return context.new_page()


@pytest.fixture
def site_page(page: Page, settings: Settings) -> Page:
    if settings.site_url is None:
        # ty mis-types pytest.skip (callable wrapper object); the call itself is correct.
        pytest.skip("SITE_BASE_URL is not configured")  # ty: ignore[too-many-positional-arguments]
    return page


@pytest.fixture
def page_with_block(
    request: pytest.FixtureRequest, api_client: ApiClient, cleanup: CleanupStack, settings: Settings
) -> tuple[ModuleSpec, dict[str, Any], dict[str, Any]]:
    """Create a block of the parametrised type and a page template that embeds it.

    Returns ``(block spec, block payload, created block)``.
    """
    if settings.site_url is None:
        # ty mis-types pytest.skip (callable wrapper object); the call itself is correct.
        pytest.skip("SITE_BASE_URL is not configured")  # ty: ignore[too-many-positional-arguments]
    block = spec(request.param)
    pages = spec("pages")
    with allure.step(f"Create a {block.key} block and a page that embeds it"):
        block_payload, created_block = create_entity(api_client, cleanup, block)
        page_payload = build_payload(pages.request_model)
        page_payload["url"] = settings.test_page_path.strip("/")
        page_payload["blocks"][0].update(
            blockType=block.block_type, blockTemplateId=created_block["id"]
        )
        create_entity(api_client, cleanup, pages, page_payload)
    return block, block_payload, created_block


# -- reporting -----------------------------------------------------------------------------


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    """Attach a screenshot and the URL to Allure when a browser test fails."""
    report = yield
    if report.when != "call" or not report.failed:
        return report
    for name in ("cms_page", "site_page", "page"):
        page = getattr(item, "funcargs", {}).get(name)
        if isinstance(page, Page) and not page.is_closed():
            with contextlib.suppress(Exception):
                Attachments.text(page.url, "Page URL")
                Attachments.screenshot(page, "Screenshot on failure")
            break
    return report


def _git_sha() -> str:
    if sha := os.getenv("GITHUB_SHA"):
        return sha[:12]
    try:
        # Fixed argv, no shell: safe to run in CI and locally.
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def pytest_sessionfinish(session: pytest.Session) -> None:
    """Write ``environment.properties`` so the report shows how to replay the run."""
    if hasattr(session.config, "workerinput"):
        return  # xdist worker: the controller writes the file
    alluredir = session.config.getoption("--alluredir", default=None)
    if not alluredir:
        return
    properties: dict[str, Any] = {
        "faker.seed": session.config.stash.get(FAKER_SEED_KEY, "n/a"),
        "browser": ",".join(session.config.option.browser or ["chromium"]),
        "git.sha": _git_sha(),
    }
    with contextlib.suppress(Exception):  # settings may be absent, e.g. on --collect-only
        settings = get_settings()
        properties["api.host"] = settings.api_url
        properties["viewport"] = settings.viewport
    target = Path(alluredir)
    target.mkdir(parents=True, exist_ok=True)
    (target / "environment.properties").write_text(
        "".join(f"{key}={value}\n" for key, value in properties.items()), encoding="utf-8"
    )
