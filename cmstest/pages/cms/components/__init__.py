"""Reusable widgets of the admin panel. Each takes the form's :class:`CmsPage` or ``Page``."""

from cmstest.pages.cms.components.buttons import Buttons
from cmstest.pages.cms.components.color_picker import ColorPicker
from cmstest.pages.cms.components.dropdown import DropDown
from cmstest.pages.cms.components.indexing import Indexing
from cmstest.pages.cms.components.text_editor import TextEditor
from cmstest.pages.cms.components.video_loader import Video

__all__ = ["Buttons", "ColorPicker", "DropDown", "Indexing", "TextEditor", "Video"]
