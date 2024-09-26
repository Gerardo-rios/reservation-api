from dataclasses import dataclass


@dataclass
class CreatePersonResponse:
    person_id: str


@dataclass
class GetPersonResponse:
    person_id: str
    name: str
    phone: str
    address: str
    city: str
    country: str
