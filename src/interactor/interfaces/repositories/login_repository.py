from abc import ABC, abstractmethod
from typing import Optional

from src.domain import LoginSession


class LoginRepositoryInterface(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> Optional[LoginSession]:
        pass
