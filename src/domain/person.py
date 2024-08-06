from dataclasses import asdict, dataclass
from uuid import UUID
from typing import Dict, Any


@dataclass
class Person:
    person_id: UUID
    name: str
    phone: str
    address: str
    city: str
    country: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Person":
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
