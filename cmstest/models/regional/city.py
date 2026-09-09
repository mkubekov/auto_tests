"""City with an office: main address, extra addresses and legal requisites."""

from __future__ import annotations

from pydantic import BaseModel, Field

from cmstest.data.generators import fake
from cmstest.models.common import BaseFields


def _work_time() -> str:
    return f"{fake.time('%H:%M')}-{fake.time('%H:%M')}"


class Address(BaseModel):
    email: str = Field(default_factory=lambda: fake.email())
    metro: str = Field(default_factory=lambda: fake.street_name())
    phone: str = Field(default_factory=lambda: fake.phone_number())
    address: str = Field(default_factory=lambda: fake.address().replace("\n", ", "))
    workTime: str = Field(default_factory=_work_time)
    isPhoneCalltracking: bool = Field(default_factory=lambda: fake.boolean())


class Requisite(BaseModel):
    name: str = Field(default_factory=lambda: fake.word())
    value: str = Field(default_factory=lambda: str(fake.random_number(digits=10)))


class City(BaseFields):
    city: str = Field(default_factory=lambda: fake.city())
    actualAddress: Address = Field(default_factory=Address)
    requisites: list[Requisite] = Field(default_factory=lambda: [Requisite()])
    multiAddress: bool = Field(default_factory=lambda: fake.boolean())
    secondaryAddresses: list[Address] = Field(default_factory=lambda: [Address()])
    hasCenter: bool = Field(default_factory=lambda: fake.boolean())
    regionName: str = Field(default_factory=lambda: fake.administrative_unit())
    regionId: str = Field(default_factory=lambda: fake.uuid4())
    cityGuid: str = Field(default_factory=lambda: fake.uuid4())
