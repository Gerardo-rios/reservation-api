from dataclasses import asdict, dataclass
from typing import Any, Dict

from src.domain import Session


@dataclass
class LoginInputDto:
    email: str
    password: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LoginOutputDto:
    token: str
    session: Session
