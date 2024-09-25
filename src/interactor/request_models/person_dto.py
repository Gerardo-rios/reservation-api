from dataclasses import dataclass


@dataclass
class CreatePersonRequest:
    name: str
    phone: str
    address: str


@dataclass
class GetPersonByPhoneRequest:
    phone: str
