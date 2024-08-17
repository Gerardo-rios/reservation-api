from dataclasses import dataclass, asdict
from typing import Dict, Any
from src.domain import Account, Person


@dataclass
class CreateAccountInputDto:
    email: str
    password: str
    user: str
    photo: str
    role_id: str
    person: Person

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CreateAccountOutputDto:
    account: Account
    person: Person
    role_id: str
