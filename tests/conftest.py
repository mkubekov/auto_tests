"""Root conftest: only what every test layer needs and what works without a stand.

Network and browser fixtures live in ``tests/e2e/conftest.py`` so that ``tests/unit`` runs
without any configuration.
"""

from __future__ import annotations

import os
import random

import pytest
from faker import Faker

# StashKey instead of an ad-hoc attribute on Config: the typed, supported mechanism.
FAKER_SEED_KEY = pytest.StashKey[int]()


def pytest_configure(config: pytest.Config) -> None:
    """Pin the Faker seed; otherwise a failure on generated data cannot be reproduced."""
    env_seed = os.getenv("FAKER_SEED")
    # Not cryptographic: the seed only drives test data generation.
    seed = int(env_seed) if env_seed else random.randrange(2**32)  # noqa: S311
    Faker.seed(seed)
    config.stash[FAKER_SEED_KEY] = seed


def pytest_report_header(config: pytest.Config) -> str:
    seed = config.stash[FAKER_SEED_KEY]
    return f"faker seed: {seed} (set FAKER_SEED={seed} to replay this run)"
