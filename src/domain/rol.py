from dataclasses import asdict, dataclass
from uuid import UUID
from typing import Dict, Any


@dataclass
class Rol:
    rol_id: UUID
    rol_name: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rol":
        return cls(**data)

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)
