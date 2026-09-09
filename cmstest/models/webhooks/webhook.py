"""Webhook integration: the minimal two-field module, a good starting point for new ones."""

from __future__ import annotations

from pydantic import Field

from cmstest.data.generators import fake
from cmstest.models.common import BaseFields


class Webhook(BaseFields):
    externalId: str = Field(default_factory=lambda: fake.bothify(text="EXT-####-####"))
    campaignCode: str = Field(default_factory=lambda: fake.bothify(text="CMP-####-####"))
