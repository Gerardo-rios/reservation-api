from abc import ABC, abstractmethod
from typing import Any, Dict

from src.interactor import response_models


class GetAccountControllerInterface(ABC):
    @abstractmethod
    def create_request_data(self, json_input_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def execute(self) -> response_models.GetAccountResponse:
        pass
