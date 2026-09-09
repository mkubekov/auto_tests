"""City form: tabs for the main address, requisites and additional addresses.

Unlike other forms this one is submitted with a primary "Add" button and confirms with a
notification, so :meth:`save` is overridden.
"""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.pages.cms.base import CmsPage

ADDRESS_FIELDS = ("address", "email", "metro", "workTime", "phone")


class City(CmsPage):
    _city = '[id="city"]'
    _region_name = '[id="regionName"]'
    _region_id = '[id="regionId"]'
    _city_guid = '[id="cityGuid"]'
    _multi_address = '[id="multiAddress"]'
    _tab_requisites = "Requisites"
    _tab_addresses = "Additional addresses"
    _add_row = labels.ADD

    @staticmethod
    def _address_field(prefix: str, field: str) -> str:
        return f'[id="{prefix}_{field}"]'

    def fill_address(self, caption: str, prefix: str, address: dict[str, Any]) -> Self:
        with allure.step(caption):
            for field in ADDRESS_FIELDS:
                self.fill(field, self._address_field(prefix, field), address[field])
            if "isPhoneCalltracking" in address:
                self.switch(
                    "Call tracking",
                    self._address_field(prefix, "isPhoneCalltracking"),
                    address["isPhoneCalltracking"],
                )
        return self

    def fill_requisites(self, requisites: list[dict[str, Any]]) -> Self:
        self.switch_tab(self._tab_requisites)
        for index, requisite in enumerate(requisites):
            with allure.step(f"Requisite {index + 1}"):
                self.click_dashed(self._add_row)
                self.fill("Requisite name", f'[id="requisites_{index}_name"]', requisite["name"])
                self.fill("Requisite value", f'[id="requisites_{index}_value"]', requisite["value"])
        return self

    def fill_secondary_addresses(self, addresses: list[dict[str, Any]]) -> Self:
        self.switch_tab(self._tab_addresses)
        self.switch("Several addresses", self._multi_address, True)
        for index, address in enumerate(addresses):
            self.click_dashed(self._add_row)
            self.fill_address(
                f"Additional address {index + 1}", f"secondaryAddresses_{index}", address
            )
        return self

    def save(self) -> Self:
        with allure.step("Save"):
            self.page.on("response", self._capture_created_id)
            try:
                self.page.locator('[type="submit"]').get_by_text(labels.ADD).click()
                self.page.locator(".ant-notification-notice-message").wait_for(state="visible")
            finally:
                self.page.remove_listener("response", self._capture_created_id)
        return self

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create city"):
            self.fill("City", self._city, payload["city"])
            self.fill_address("Main address", "actualAddress", payload["actualAddress"])
            self.fill("Region name", self._region_name, payload["regionName"])
            self.fill("Region id", self._region_id, payload["regionId"])
            self.fill("City GUID", self._city_guid, payload["cityGuid"])
            if payload["requisites"]:
                self.fill_requisites(payload["requisites"])
            if payload["multiAddress"] and payload["secondaryAddresses"]:
                self.fill_secondary_addresses(payload["secondaryAddresses"])
            self.save()
        return self

    def _check_address(self, caption: str, sent: dict[str, Any], received: dict[str, Any]) -> None:
        with allure.step(caption):
            for field in ADDRESS_FIELDS:
                self.check_item(field, sent[field], received[field])

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item("City", payload["city"], created["city"])
        self.check_item("Region name", payload["regionName"], created["regionName"])
        self.check_item("Region id", payload["regionId"], created["regionId"])
        self.check_item("City GUID", payload["cityGuid"], created["cityGuid"])
        self._check_address("Main address", payload["actualAddress"], created["actualAddress"])
        self.check_item(
            "Call tracking",
            payload["actualAddress"]["isPhoneCalltracking"],
            created["actualAddress"]["isPhoneCalltracking"],
        )
        for index, requisite in enumerate(payload["requisites"]):
            with allure.step(f"Requisite {index + 1}"):
                got = created["requisites"][index]
                self.check_item("Requisite name", requisite["name"], got["name"])
                self.check_item("Requisite value", requisite["value"], got["value"])
        if payload["multiAddress"]:
            for index, address in enumerate(payload["secondaryAddresses"]):
                self._check_address(
                    f"Additional address {index + 1}", address, created["secondaryAddresses"][index]
                )
        return self
