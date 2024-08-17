from abc import ABC, abstractmethod
from typing import Optional
from src.domain import Role


class RoleRepositoryInterface(ABC):
    @abstractmethod
    def get(self, role_name: str) -> Optional[Role]:
        pass
