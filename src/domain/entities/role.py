from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class Role:
    role_id: str
    role_name: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Role":
        return cls(**data)

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)
