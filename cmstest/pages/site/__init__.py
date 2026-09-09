"""Public-site page objects (scaffold: locators are project-specific)."""

from cmstest.pages.site.base import SitePage
from cmstest.pages.site.page_constructor.gallery_block import GalleryBlock
from cmstest.pages.site.page_constructor.page import Page
from cmstest.pages.site.page_constructor.text_block import TextBlock

__all__ = ["GalleryBlock", "Page", "SitePage", "TextBlock"]
