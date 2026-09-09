"""Footer: composed of existing footer sections referenced by object."""

from __future__ import annotations

from pydantic import Field

from cmstest.http.references import references
from cmstest.models.common import BaseFields, Reference


class Footer(BaseFields):
    sections: list[Reference] = Field(
        default_factory=lambda: [references().first("footer_sections")]
    )
