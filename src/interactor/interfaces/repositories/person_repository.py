from abc import ABC, abstractmethod
from typing import Optional
from src.domain import Person


class PersonRepositoryInterface(ABC):
    @abstractmethod
    def create(self, person: Person) -> Optional[Person]:
        pass

    @abstractmethod
    def get(self, person_id: str) -> Optional[Person]:
        pass

    @abstractmethod
    def update(self, person: Person) -> Optional[Person]:
        pass

    @abstractmethod
    def delete(self, person_id: str) -> bool:
        pass
