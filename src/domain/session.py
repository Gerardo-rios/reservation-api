from dataclasses import asdict, dataclass
from typing import Any, Dict

from . import Account, Person, Role


@dataclass
class Session:
    account: Account
    person: Person
    role: Role

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        return cls(**data)

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)
