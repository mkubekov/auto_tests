"""Statistics block form: rich-text heading and a list of metric cards."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import TextEditor


class Statistic(CmsPage):
    @staticmethod
    def _metric_title(index: int) -> str:
        return f'[id="statBlock__{index}_title"]'

    @staticmethod
    def _metric_text(index: int) -> str:
        return f'[id="statBlock__{index}_text"]'

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create statistics block"):
            self.fill_name(payload["name"])
            TextEditor(self.page, "Title", self._title).type(payload["title"])
            TextEditor(self.page, "Subtitle", self._subtitle).type(payload["subtitle"])
            for index, metric in enumerate(payload["statBlocks"]):
                with allure.step(f"Metric {index + 1}"):
                    TextEditor(self.page, "Metric", self._metric_title(index)).type(metric["title"])
                    TextEditor(self.page, "Description", self._metric_text(index)).type(
                        metric["text"]
                    )
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_text("Title", payload["title"], created["title"])
        self.check_text("Subtitle", payload["subtitle"], created["subtitle"])
        for index, metric in enumerate(payload["statBlocks"]):
            with allure.step(f"Metric {index + 1}"):
                self.check_text("Metric", metric["title"], created["statBlocks"][index]["title"])
                self.check_text("Description", metric["text"], created["statBlocks"][index]["text"])
        return self
