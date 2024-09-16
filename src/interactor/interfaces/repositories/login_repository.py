from abc import ABC, abstractmethod
from typing import Optional

from src.domain import Account


class LoginRepositoryInterface(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> Optional[Account]:
        pass
