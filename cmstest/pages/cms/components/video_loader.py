"""Video widget: upload a file or paste a link, plus a poster image."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from cmstest.data.files import VIDEO_MP4

if TYPE_CHECKING:
    from cmstest.pages.cms.base import CmsPage


class Video:
    """``prefix`` scopes the field ids when the widget is repeated inside a list."""

    def __init__(self, form: CmsPage, prefix: str = "") -> None:
        self.form = form
        self.prefix = prefix

    def _id(self, field: str) -> str:
        return f'[id="{self.prefix}{field}"]'

    def _for(self, field: str) -> str:
        return f'[for="{self.prefix}{field}"]'

    def switch_source(self, by_link: bool) -> Self:
        self.form.switch("Video by link", self._id("videoLinkType"), by_link)
        return self

    def upload(self, file_name: str = VIDEO_MP4, field: str = "src") -> Self:
        self.form.upload("Video", self._for(field), file_name)
        return self

    def fill_link(self, url: str, field: str = "src") -> Self:
        self.form.fill("Video link", self._id(field), url)
        return self

    def upload_poster(self, file_name: str, field: str = "previewImageSrc") -> Self:
        self.form.upload("Poster", self._for(field), file_name)
        return self

    def check(self, sent: dict[str, Any], received: dict[str, Any]) -> Self:
        self.form.check_file("Video", sent["videoLink"], received["videoLink"])
        self.form.check_file("Poster", sent["imageLink"], received["imageLink"])
        return self
