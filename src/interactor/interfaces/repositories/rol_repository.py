from abc import ABC, abstractmethod
from typing import Optional
from src.domain import Rol


class RolRepositoryInterface(ABC):
    @abstractmethod
    def get(self, rol_id: str) -> Optional[Rol]:
        pass
