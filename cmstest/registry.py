"""The registry: one :class:`ModuleSpec` binds a CMS module across all three layers.

Tests are parametrised from this dict, so adding a module here is what puts it under test.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from _pytest.mark.structures import ParameterSet  # pytest.param() return type, not re-exported
from pydantic import BaseModel

from cmstest import models
from cmstest.pages import cms, site
from cmstest.pages.cms.base import CmsPage
from cmstest.pages.site.base import SitePage


@dataclass(frozen=True, slots=True)
class ModuleSpec:
    key: str
    api_path: str
    request_model: type[BaseModel]
    cms_path: str | None = None
    cms_page: type[CmsPage] | None = None
    site_page: type[SitePage] | None = None
    #: Discriminator used by page templates to embed this block (page-constructor blocks only).
    block_type: str | None = None
    #: ``False`` for entities that need related entities first; they get dedicated tests.
    standalone: bool = True
    #: Field changed by the PATCH test.
    patch_field: str = "name"
    #: Why the admin-panel test is skipped. Shown in the report instead of a silent skip.
    cms_skip_reason: str | None = None

    @property
    def has_cms(self) -> bool:
        return self.cms_page is not None and self.cms_path is not None


_SPECS = [
    ModuleSpec(
        key="handbooks",
        api_path="content/handbooks",
        request_model=models.Handbook,
        patch_field="value",
    ),
    ModuleSpec(
        key="webhooks",
        api_path="content/webhooks",
        request_model=models.Webhook,
        cms_path="integrations/webhooks",
        cms_page=cms.Webhook,
    ),
    ModuleSpec(
        key="statistics",
        api_path="content/statistics",
        request_model=models.Statistic,
        cms_path="blocks/statistics",
        cms_page=cms.Statistic,
    ),
    ModuleSpec(
        key="accordions",
        api_path="content/accordions",
        request_model=models.Accordion,
        cms_path="blocks/accordions",
        cms_page=cms.Accordion,
    ),
    ModuleSpec(
        key="banners",
        api_path="content/banners",
        request_model=models.Banner,
        cms_path="banners",
        cms_page=cms.Banner,
    ),
    ModuleSpec(
        key="promoBanners",
        api_path="content/promo-banners",
        request_model=models.PromoBanner,
        cms_path="promo-banners",
        cms_page=cms.PromoBanner,
        cms_skip_reason="activity period: the date-range picker is not automated yet",
    ),
    ModuleSpec(
        key="footerSections",
        api_path="content/footer-sections",
        request_model=models.FooterSection,
        cms_path="footer/sections",
        cms_page=cms.FooterSection,
    ),
    ModuleSpec(
        key="footers",
        api_path="content/footers",
        request_model=models.Footer,
        cms_path="footer",
        cms_page=cms.Footer,
    ),
    ModuleSpec(
        key="headerSubcategories",
        api_path="content/header-subcategories",
        request_model=models.HeaderSubcategory,
        cms_path="header/subcategories",
        cms_page=cms.HeaderSubcategory,
    ),
    ModuleSpec(
        key="headerCategories",
        api_path="content/header-categories",
        request_model=models.HeaderCategory,
        cms_path="header/categories",
        cms_page=cms.HeaderCategory,
        cms_skip_reason="nested subcategory widgets are not verified against a live admin panel",
    ),
    ModuleSpec(
        key="headers",
        api_path="content/headers",
        request_model=models.Header,
        cms_path="header",
        cms_page=cms.Header,
        standalone=False,  # needs a category first: see tests/e2e/api/test_header.py
    ),
    ModuleSpec(
        key="cities",
        api_path="content/cities",
        request_model=models.City,
        cms_path="locations/cities",
        cms_page=cms.City,
    ),
    ModuleSpec(
        key="videoLessons",
        api_path="content/video-lessons",
        request_model=models.VideoLessons,
        cms_path="video-lessons",
        cms_page=cms.VideoLessons,
    ),
    ModuleSpec(
        key="textBlocks",
        api_path="content/page-constructor/text-block-templates",
        request_model=models.TextBlock,
        cms_path="page-constructor/text-block-templates",
        cms_page=cms.TextBlock,
        site_page=site.TextBlock,
        block_type="textBlock",
    ),
    ModuleSpec(
        key="galleryBlocks",
        api_path="content/page-constructor/gallery-block-templates",
        request_model=models.GalleryBlock,
        cms_path="page-constructor/gallery-block-templates",
        cms_page=cms.GalleryBlock,
        site_page=site.GalleryBlock,
        block_type="galleryBlock",
    ),
    ModuleSpec(
        key="pages",
        api_path="content/page-constructor/page-templates",
        request_model=models.Page,
        cms_path="page-constructor/page-templates",
        cms_page=cms.Page,
        site_page=site.Page,
    ),
]

MODULES: dict[str, ModuleSpec] = {spec.key: spec for spec in _SPECS}


def spec(key: str) -> ModuleSpec:
    return MODULES[key]


def api_params() -> list[ParameterSet]:
    """Every module, for read-only API checks."""
    return [pytest.param(key, id=key) for key in MODULES]


def writable_params() -> list[ParameterSet]:
    """Modules that can be created on their own, for generic write/negative API checks."""
    return [pytest.param(key, id=key) for key, module in MODULES.items() if module.standalone]


def cms_params() -> list[ParameterSet]:
    """Modules with an admin form; skip reasons become collection-time marks."""
    params = []
    for key, module in MODULES.items():
        if not module.has_cms:
            continue
        marks = [pytest.mark.skip(reason=module.cms_skip_reason)] if module.cms_skip_reason else []
        params.append(pytest.param(key, id=key, marks=marks))
    return params


def page_block_params() -> list[ParameterSet]:
    """Page-constructor blocks that have a public-site page object."""
    return [
        pytest.param(key, id=key)
        for key, module in MODULES.items()
        if module.block_type and module.site_page is not None
    ]
