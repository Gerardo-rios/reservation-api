from typing import Any, Dict
from abc import ABC, abstractmethod
from src.interactor import CreatePersonOutputDto


class CreatePersonPresenterInterface(ABC):
    @abstractmethod
    def present(self, output_dto: CreatePersonOutputDto) -> Dict[str, Any]:
        pass
