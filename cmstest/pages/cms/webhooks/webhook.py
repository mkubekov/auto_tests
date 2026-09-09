"""Webhook form: the minimal page object, a good template for new modules."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.base import CmsPage


class Webhook(CmsPage):
    _external_id = '[id="externalId"]'
    _campaign_code = '[id="campaignCode"]'

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create webhook"):
            self.fill_name(payload["name"])
            self.fill("External id", self._external_id, payload["externalId"])
            self.fill("Campaign code", self._campaign_code, payload["campaignCode"])
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_item("External id", payload["externalId"], created["externalId"])
        self.check_item("Campaign code", payload["campaignCode"], created["campaignCode"])
        return self
