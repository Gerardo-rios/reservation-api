from uuid import UUID
from dataclasses import dataclass, asdict
from typing import Dict, Any
from src.domain import Account


@dataclass
class CreateAccountInputDto:
    email: str
    password: str
    user: str
    photo: str
    rol_id: UUID
    person_id: UUID

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CreateAccountOutputDto:
    account: Account
