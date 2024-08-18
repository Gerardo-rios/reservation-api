from abc import ABC, abstractmethod
from typing import Any, Dict

from src.interactor.dtos import LoginOutputDto


class LoginPresenterInterface(ABC):
    @abstractmethod
    def present(self, output_dto: LoginOutputDto) -> Dict[str, Any]:
        pass
