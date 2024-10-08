from abc import ABC, abstractmethod
from typing import Any, Dict


class GetAccountControllerInterface(ABC):
    @abstractmethod
    def create_request_data(self, json_input_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        pass
