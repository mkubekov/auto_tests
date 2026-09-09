"""Video lessons page form: hero section, SEO meta, colour and a list of videos."""

from __future__ import annotations

from typing import Any, Self

import allure

from cmstest.data import labels
from cmstest.data.files import VIDEO_MP4
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.components import ColorPicker, DropDown, Video


class VideoLessons(CmsPage):
    _external_name = '[id="externalName"]'
    _block_color = '[for="blockColor"]'
    _hero_title = '[id="firstScreen.title"]'
    _hero_subtitle = '[id="firstScreen.subtitle"]'
    _hero_button = '[id="firstScreen.btnText"]'
    _hero_image = '[for="firstScreen.imageUrl"]'
    _no_index = '[id="noIndex"]'
    _meta_title = '[id="meta.title"]'
    _meta_description = '[id="meta.description"]'
    _video_title = '[id="videoTitle"]'
    _add_video = "Add video"

    @staticmethod
    def _video_field(index: int, field: str) -> str:
        return f'[id="videos_{index}_{field}"]'

    def fill_hero(self, hero: dict[str, Any]) -> Self:
        with allure.step("Hero section"):
            self.fill("Title", self._hero_title, hero["title"])
            self.fill("Subtitle", self._hero_subtitle, hero["subtitle"])
            self.fill("Button text", self._hero_button, hero["btnText"])
            self.upload("Image", self._hero_image, hero["imageUrl"])
        return self

    def fill_meta(self, meta: dict[str, Any]) -> Self:
        with allure.step("SEO meta"):
            self.switch("No index", self._no_index, meta["noIndex"])
            self.fill("Meta title", self._meta_title, meta["title"])
            self.fill("Meta description", self._meta_description, meta["description"])
        return self

    def add_video(self, index: int, video: dict[str, Any]) -> Self:
        with allure.step(f"Video {index + 1}"):
            self.click_dashed(self._add_video)
            self.fill("Video title", self._video_field(index, "title"), video["title"])
            self.fill(
                "Video description", self._video_field(index, "description"), video["description"]
            )
            widget = Video(self, prefix=f"videos_{index}_")
            widget.upload(VIDEO_MP4, field="videoLink")
            widget.upload_poster(video["imageLink"], field="imageLink")
            for label in video["labels"]:
                DropDown(self.page, "Labels", self._video_field(index, "labels")).set(label)
        return self

    def create_element(self, payload: dict[str, Any]) -> Self:
        with allure.step("Create video lessons page"):
            self.fill_name(payload["name"])
            self.fill("External name", self._external_name, payload["externalName"])
            self.fill("URL", self._url, payload["url"])
            ColorPicker(self).set("Block colour", self._block_color, payload["blockColor"])
            self.fill_hero(payload["firstScreen"])
            self.fill_meta(payload["meta"])
            self.fill("Videos title", self._video_title, payload["videoTitle"])
            for index, video in enumerate(payload["videos"]):
                self.add_video(index, video)
            self.save()
        return self

    def check_created_item(self, payload: dict[str, Any], created: dict[str, Any]) -> Self:
        self.check_item(labels.SYSTEM_NAME, payload["name"], created["name"])
        self.check_item("External name", payload["externalName"], created["externalName"])
        self.check_item("URL", payload["url"], created["url"])
        hero, got_hero = payload["firstScreen"], created["firstScreen"]
        self.check_item("Hero title", hero["title"], got_hero["title"])
        self.check_item("Hero subtitle", hero["subtitle"], got_hero["subtitle"])
        self.check_item("Hero button", hero["btnText"], got_hero["btnText"])
        self.check_file("Hero image", hero["imageUrl"], got_hero["imageUrl"])
        meta, got_meta = payload["meta"], created["meta"]
        self.check_item("No index", meta["noIndex"], got_meta["noIndex"])
        self.check_item("Meta title", meta["title"], got_meta["title"])
        self.check_item("Meta description", meta["description"], got_meta["description"])
        self.check_item("Videos title", payload["videoTitle"], created["videoTitle"])
        for index, video in enumerate(payload["videos"]):
            with allure.step(f"Video {index + 1}"):
                got = created["videos"][index]
                self.check_item("Video title", video["title"], got["title"])
                self.check_item("Video description", video["description"], got["description"])
                self.check_file("Poster", video["imageLink"], got["imageLink"])
                for position, label in enumerate(video["labels"]):
                    self.check_item("Label", label, got["labels"][position])
        return self
