from typing import Any, Dict
from abc import ABC, abstractmethod


class AccountControllerInterface(ABC):
    @abstractmethod
    def create_account_info(self, json_input_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        pass
