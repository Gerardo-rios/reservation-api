from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class LoginSession:
    account: Dict[str, Any]
    person: Dict[str, Any]
    role: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LoginSession":
        return cls(**data)

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)
