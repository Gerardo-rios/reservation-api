from dataclasses import dataclass, asdict
from typing import Dict, Any
from src.domain import Person


@dataclass
class CreatePersonInputDto:
    name: str
    phone: str
    address: str
    city: str
    country: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CreatePersonOutputDto:
    person: Person
