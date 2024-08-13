from abc import ABC, abstractmethod
from typing import Optional
from src.domain import Person


class PersonRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self, name: str, phone: str, address: str, city: str, country: str
    ) -> Optional[Person]:
        pass

    @abstractmethod
    def get(self, person_id: str) -> Optional[Person]:
        pass

    @abstractmethod
    def update(self, person: Person) -> Optional[Person]:
        pass
