from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class Account:
    account_id: str
    email: str
    password: str
    user: str
    photo: str
    status: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Account":
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
