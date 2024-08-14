from dataclasses import dataclass, asdict
from typing import Dict, Any
from src.domain import Account


@dataclass
class CreateAccountInputDto:
    email: str
    password: str
    user: str
    photo: str
    role_id: str
    person_id: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CreateAccountOutputDto:
    account: Account
    role_id: str
    person_id: str
