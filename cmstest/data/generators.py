"""Faker instance and per-run identifiers.

The locale is read from ``FAKER_LOCALE`` directly rather than from ``Settings`` so that
importing a model never requires a fully configured environment (unit tests rely on this).
"""

from __future__ import annotations

import os
from uuid import uuid4

from faker import Faker

FAKER_LOCALE = os.getenv("FAKER_LOCALE", "en_US")

fake = Faker(FAKER_LOCALE)

# Unique per process. Cleanup searches by this marker, so a run never deletes entities
# created by another run (or by another xdist worker) on a shared stand.
RUN_ID = uuid4().hex[:8]


def run_marker() -> str:
    """Prefix shared by every entity created in this process."""
    return f"autotest-{RUN_ID}"


def unique_name() -> str:
    """Entity name: run marker plus a short suffix, so a lookup by name is unambiguous."""
    return f"{run_marker()}-{uuid4().hex[:6]}"
