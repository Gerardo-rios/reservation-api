from dataclasses import asdict, dataclass
from typing import Any, Dict

from src.domain import Role


@dataclass
class GetRoleInputDto:
    role_name: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GetRoleOutputDto:
    role: Role
