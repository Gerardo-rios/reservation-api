from dataclasses import dataclass


@dataclass
class Person:
    person_id: str
    name: str
    phone: str
    address: str
    city: str
    country: str
