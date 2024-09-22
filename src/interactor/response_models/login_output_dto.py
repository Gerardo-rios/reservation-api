from dataclasses import dataclass
from typing import Optional


@dataclass
class LoginResponse:
    account: str
    token: Optional[str] = None
