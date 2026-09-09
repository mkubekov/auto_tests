"""Admin-panel page objects. Each implements ``create_element`` and ``check_created_item``."""

from cmstest.pages.cms.banners.banner import Banner
from cmstest.pages.cms.banners.promo_banner import PromoBanner
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.cms.blocks.accordion import Accordion
from cmstest.pages.cms.blocks.statistic import Statistic
from cmstest.pages.cms.footer.footer import Footer
from cmstest.pages.cms.footer.footer_section import FooterSection
from cmstest.pages.cms.header.header import Header
from cmstest.pages.cms.header.header_category import HeaderCategory
from cmstest.pages.cms.header.header_subcategory import HeaderSubcategory
from cmstest.pages.cms.page_constructor.gallery_block import GalleryBlock
from cmstest.pages.cms.page_constructor.page import Page
from cmstest.pages.cms.page_constructor.text_block import TextBlock
from cmstest.pages.cms.regional.city import City
from cmstest.pages.cms.sections.video_lessons import VideoLessons
from cmstest.pages.cms.webhooks.webhook import Webhook

__all__ = [
    "Accordion",
    "Banner",
    "City",
    "CmsPage",
    "Footer",
    "FooterSection",
    "GalleryBlock",
    "Header",
    "HeaderCategory",
    "HeaderSubcategory",
    "Page",
    "PromoBanner",
    "Statistic",
    "TextBlock",
    "VideoLessons",
    "Webhook",
]
