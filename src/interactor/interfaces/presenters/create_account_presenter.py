from abc import ABC, abstractmethod
from typing import Any, Dict

from src.interactor import CreateAccountOutputDto


class CreateAccountPresenterInterface(ABC):
    @abstractmethod
    def present(self, output_dto: CreateAccountOutputDto) -> Dict[str, Any]:
        pass
