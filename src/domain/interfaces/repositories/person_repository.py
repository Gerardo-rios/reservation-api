from abc import ABC, abstractmethod
from typing import Optional

from src.domain import Person


class PersonRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self, name: str, phone: str, address: str, city: str, country: str
    ) -> Optional[str]:
        pass

    @abstractmethod
    def find_by_phone(self, phone: str) -> Optional[Person]:
        pass