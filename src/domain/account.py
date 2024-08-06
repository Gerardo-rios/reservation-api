from dataclasses import asdict, dataclass
from uuid import UUID
from typing import Dict, Any


@dataclass
class Account:
    account_id: UUID
    email: str
    password: str
    user: str
    photo: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Account":
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
