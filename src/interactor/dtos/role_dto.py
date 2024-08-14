from dataclasses import dataclass, asdict
from typing import Dict, Any
from src.domain import Role


@dataclass
class GetRoleInputDto:
    role_name: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GetRoleOutputDto:
    role: Role
