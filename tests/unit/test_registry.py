from pydantic import BaseModel

from cmstest.http.references import DEFAULT_REFERENCE_PATHS
from cmstest.pages.cms.base import CmsPage
from cmstest.registry import (
    MODULES,
    api_params,
    cms_params,
    page_block_params,
    writable_params,
)


def test_keys_match_spec_keys() -> None:
    assert all(key == module.key for key, module in MODULES.items())


def test_every_module_has_a_request_model() -> None:
    assert all(issubclass(module.request_model, BaseModel) for module in MODULES.values())


def test_cms_page_and_cms_path_come_together() -> None:
    for module in MODULES.values():
        assert (module.cms_page is None) == (module.cms_path is None), module.key


def test_cms_pages_implement_the_contract() -> None:
    for module in MODULES.values():
        if module.cms_page is None:
            continue
        assert module.cms_page.create_element is not CmsPage.create_element, module.key
        assert module.cms_page.check_created_item is not CmsPage.check_created_item, module.key


def test_block_type_is_reserved_for_page_constructor_blocks() -> None:
    for module in MODULES.values():
        if module.block_type:
            assert "page-constructor" in module.api_path, module.key


def test_skip_reason_only_makes_sense_with_a_cms_page() -> None:
    for module in MODULES.values():
        if module.cms_skip_reason:
            assert module.has_cms, module.key


def test_param_helpers_reflect_the_registry() -> None:
    assert [param.id for param in api_params()] == list(MODULES)
    assert "headers" not in [param.id for param in writable_params()]
    skipped = {param.id for param in cms_params() if param.marks}
    assert skipped == {key for key, module in MODULES.items() if module.cms_skip_reason}
    assert {param.id for param in page_block_params()} == {"textBlocks", "galleryBlocks"}


def test_reference_paths_point_at_registered_modules() -> None:
    api_paths = {module.api_path for module in MODULES.values()}
    for key, path in DEFAULT_REFERENCE_PATHS.items():
        assert path.split("?")[0] in api_paths, key
