from abc import ABC, abstractmethod
from typing import Optional
from src.domain import Rol


class RolRepositoryInterface(ABC):
    @abstractmethod
    def get(self, role_name: str) -> Optional[Rol]:
        pass

    @abstractmethod
    def create(
        self, role_name: Optional[str] = None, description: Optional[str] = None
    ) -> Optional[Rol]:
        pass
