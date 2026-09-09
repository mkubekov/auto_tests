"""Gallery block form: repeatable slides with media, rich text and breakpoint offsets."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.data.files import VIDEO_MP4
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import TextEditor, Video

BREAKPOINTS = ("ultraHD", "fullHD", "desktop", "tablet", "pad", "mobile")


class GalleryBlock(CmsPage):
    _add_slide = "Add slide"

    @staticmethod
    def _slide(index: int, field: str) -> str:
        return f'[id="galleryList_{index}_{field}"]'

    def add_slide(self, index: int, slide: dict[str, Any]) -> Self:
        with allure.step(f"Slide {index + 1}"):
            self.click_dashed(self._add_slide)
            media = Video(self, prefix=f"galleryList_{index}_")
            media.upload(VIDEO_MP4)
            media.upload_poster(slide["previewImageSrc"])
            TextEditor(self.page, "Slide title", self._slide(index, "title")).type(slide["title"])
            self.fill("Slide text", self._slide(index, "text"), slide["text"])
            self.switch(
                "Advertisement", self._slide(index, "isAdvertisement"), slide["isAdvertisement"]
            )
            if slide["isAdvertisement"]:
                self.fill(
                    "Tooltip title", self._slide(index, "tooltip_title"), slide["tooltip"]["title"]
                )
                self.fill(
                    "Tooltip text", self._slide(index, "tooltip_text"), slide["tooltip"]["text"]
                )
            self.fill("Duration, ms", self._slide(index, "duration"), slide["duration"])
            for size in BREAKPOINTS:
                self.fill(
                    f"Offset ({size})",
                    self._slide(index, f"offset_{size}"),
                    slide["offset"][size],
                )
        return self

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create gallery block"):
            self.fill_name(payload["name"])
            for index, slide in enumerate(payload["galleryList"]):
                self.add_slide(index, slide)
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        for index, slide in enumerate(payload["galleryList"]):
            with allure.step(f"Slide {index + 1}"):
                got = created["galleryList"][index]
                self.check_text("Slide title", slide["title"], got["title"])
                self.check_item("Slide text", slide["text"], got["text"])
                self.check_file("Media", VIDEO_MP4, got["src"])
                self.check_file("Poster", slide["previewImageSrc"], got["previewImageSrc"])
                self.check_item("Advertisement", slide["isAdvertisement"], got["isAdvertisement"])
                for size in BREAKPOINTS:
                    self.check_item(
                        f"Offset ({size})",
                        slide["offset"][size],
                        got["offset"][size],
                    )
        return self
