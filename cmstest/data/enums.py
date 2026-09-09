"""Enumerations shared by models, page objects and tests.

All value enums are ``StrEnum`` so that a member dropped into a ``str`` field serialises
without pydantic serializer warnings and compares equal to the API's plain strings.
"""

from __future__ import annotations

from enum import IntEnum, StrEnum


class HttpStatus(IntEnum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409


class BlockColor(StrEnum):
    """Colour scheme of a content block. Must match the admin panel dropdown 1:1."""

    ORANGE = "orange"
    BLUE = "blue"
    GREEN = "green"
    VIOLET = "violet"
    GREY = "grey"
    RED = "red"


class ButtonStyle(StrEnum):
    DEFAULT = "default"
    OUTLINE = "outline"


class ButtonAction(StrEnum):
    LINK = "link"


class BannerPosition(StrEnum):
    MIDDLE = "middle"
    BOTTOM = "bottom"


class PromoBannerPosition(StrEnum):
    ABOVE_HEADER = "aboveHeader"
    MIDDLE_OF_PAGE = "middleOfPage"


class PromoButtonStyle(StrEnum):
    WITH_BORDER = "withBorder"
    DEFAULT = "default"


class Audience(StrEnum):
    """Who sees a promo banner."""

    GUEST = "guest"
    MEMBER = "member"


class MenuType(StrEnum):
    NESTED = "menuNested"
    FLAT = "menuWithoutNesting"


class HeaderActionType(StrEnum):
    EXPAND = "expandMenu"
    LINK = "link"


class SubcategoryType(StrEnum):
    LIST = "list"
    DETAILED_LIST = "detailedList"


class SubcategoryAction(StrEnum):
    LINK = "link"
    NONE = "noAction"


class HandbookType(StrEnum):
    """Reference dictionaries the CMS exposes through one ``handbooks`` endpoint."""

    CATEGORIES = "categories"
    LABELS = "labels"


class Font(StrEnum):
    SANS = "HelveticaNeueCyr"
    MONO = "CascadiaCode"
