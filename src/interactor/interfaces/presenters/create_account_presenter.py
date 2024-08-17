from typing import Any, Dict
from abc import ABC, abstractmethod
from src.interactor import CreateAccountOutputDto


class CreateAccountPresenterInterface(ABC):
    @abstractmethod
    def present(self, output_dto: CreateAccountOutputDto) -> Dict[str, Any]:
        pass
