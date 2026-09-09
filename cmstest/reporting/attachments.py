"""Attach request/response details and browser state to the Allure report."""

from __future__ import annotations

import base64
import datetime
import json
from typing import Any

import allure
import curlify
from allure import attachment_type
from playwright.sync_api import Page
from requests import Response


def _dump(data: Any) -> bytes:
    return json.dumps(data, indent=4, ensure_ascii=False, default=str).encode("utf8")


class Attachments:
    @staticmethod
    def curl(response: Response) -> None:
        stamp = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        allure.attach(
            body=f"{stamp}\n{curlify.to_curl(response.request)}",
            name="curl",
            attachment_type=attachment_type.TEXT,
            extension="txt",
        )

    @staticmethod
    def headers(response: Response) -> None:
        allure.attach(
            body=_dump(dict(response.headers)),
            name="Response headers",
            attachment_type=attachment_type.JSON,
            extension="json",
        )

    @staticmethod
    def response(response: Response) -> None:
        try:
            allure.attach(
                body=_dump(response.json()),
                name="Response body",
                attachment_type=attachment_type.JSON,
                extension="json",
            )
        except ValueError:
            allure.attach(
                body=response.text.encode("utf8"),
                name="Response body",
                attachment_type=attachment_type.TEXT,
                extension="txt",
            )

    @staticmethod
    def body(data: Any, name: str = "Body") -> None:
        allure.attach(
            body=_dump(data), name=name, attachment_type=attachment_type.JSON, extension="json"
        )

    @staticmethod
    def text(data: str, name: str) -> None:
        allure.attach(body=data.encode("utf8"), name=name, attachment_type=attachment_type.TEXT)

    @staticmethod
    def screenshot(page: Page, name: str = "Screenshot") -> None:
        allure.attach(
            base64.b64encode(page.screenshot()).decode(),
            name=name,
            attachment_type=attachment_type.PNG,
        )

    @staticmethod
    def html_dump(page: Page, name: str = "Page HTML") -> None:
        allure.attach(page.content(), name=name, attachment_type=attachment_type.HTML)
