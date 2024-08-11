from uuid import UUID
from abc import ABC, abstractmethod
from typing import Optional
from src.domain import Account


class AccountRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self, account: Account, rol_id: UUID, person_id: UUID
    ) -> Optional[Account]:
        pass

    @abstractmethod
    def get(self, account_id: str) -> Optional[Account]:
        pass

    @abstractmethod
    def update(self, account: Account) -> Optional[Account]:
        pass

    @abstractmethod
    def delete(self, account_id: str) -> bool:
        pass
