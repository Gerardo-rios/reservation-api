from dataclasses import dataclass
from typing import Optional


@dataclass
class CreatePersonRequest:
    name: str
    phone: str
    address: str
    city: str
    country: str


@dataclass
class GetPersonRequest:
    person_id: Optional[str] = None
    phone: Optional[str] = None
