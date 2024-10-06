from abc import ABC, abstractmethod
from typing import Optional

from src.domain import Role


class RoleRepositoryInterface(ABC):
    @abstractmethod
    def get_by_name(self, role_name: str) -> Optional[Role]:
        pass

    @abstractmethod
    def get_by_id(self, role_id: str) -> Optional[Role]:
        pass
