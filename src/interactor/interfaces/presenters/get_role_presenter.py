from abc import ABC, abstractmethod
from typing import Any, Dict

from src.interactor import GetRoleOutputDto


class GetRolePresenterInterface(ABC):
    @abstractmethod
    def present(self, output_dto: GetRoleOutputDto) -> Dict[str, Any]:
        pass
