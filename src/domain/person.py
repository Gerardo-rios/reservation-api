from dataclasses import asdict, dataclass
from typing import Dict, Any


@dataclass
class Person:
    person_id: str
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
