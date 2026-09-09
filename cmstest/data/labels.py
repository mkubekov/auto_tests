"""Human-readable texts the admin panel renders.

Page objects click buttons and pick dropdown options by their visible text, so this module
is the single place to adapt when the CMS is localised differently. Keys of the option maps
are API values, values are what the user sees.
"""

from __future__ import annotations

from typing import Final

# Buttons and status markers of the admin panel.
SAVE: Final = "Save"
ADD: Final = "Add"
CANCEL: Final = "Cancel"
DELETE: Final = "Delete"
SUCCESS_LOCATOR: Final = '[id="success"]'

# Field captions used in Allure steps and as the anchor for file uploaders.
SYSTEM_NAME: Final = "System name"

# Dropdown option labels keyed by API value.
BLOCK_COLOR: Final[dict[str, str]] = {
    "orange": "Orange",
    "blue": "Blue",
    "green": "Green",
    "violet": "Violet",
    "grey": "Grey",
    "red": "Red",
}
BUTTON_ACTION: Final[dict[str, str]] = {"link": "Link"}
BUTTON_STYLE: Final[dict[str, str]] = {"default": "Default", "outline": "Outline"}
BANNER_POSITION: Final[dict[str, str]] = {"middle": "Below the first screen", "bottom": "Bottom"}
PROMO_BANNER_POSITION: Final[dict[str, str]] = {
    "aboveHeader": "Above the header",
    "middleOfPage": "Middle of the page",
}
PROMO_BUTTON_STYLE: Final[dict[str, str]] = {"withBorder": "With border", "default": "Default"}
AUDIENCE: Final[dict[str, str]] = {"guest": "Guests", "member": "Members"}
MENU_TYPE: Final[dict[str, str]] = {"menuNested": "Nested menu", "menuWithoutNesting": "Flat menu"}
HEADER_ACTION: Final[dict[str, str]] = {"expandMenu": "Expand (default)", "link": "Redirect"}
SUBCATEGORY_TYPE: Final[dict[str, str]] = {"list": "Simple list", "detailedList": "Detailed list"}
SUBCATEGORY_ACTION: Final[dict[str, str]] = {"link": "Redirect", "noAction": "None (default)"}
BLOCK_TYPE: Final[dict[str, str]] = {"textBlock": "Text block", "galleryBlock": "Gallery block"}
OFFSET: Final[dict[str, str]] = {"small": "Narrow", "medium": "Regular"}
