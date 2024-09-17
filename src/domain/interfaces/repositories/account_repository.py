from abc import ABC, abstractmethod
from typing import Optional

from src.domain import Account, Person


class AccountRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self,
        email: str,
        password: str,
        user: str,
        photo: str,
        status: bool,
        role_id: str,
        person: Person,
    ) -> Optional[Account]:
        pass

    @abstractmethod
    def get(self, account_id: str) -> Optional[Account]:
        pass

    @abstractmethod
    def update(self, account: Account) -> Optional[Account]:
        pass