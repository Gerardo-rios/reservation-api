from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.domain.request_models import LoginOutputDto


class LoginPresenterInterface(ABC):
    @abstractmethod
    def present(
        self, output_dto: LoginOutputDto, token: Optional[str] = None
    ) -> Dict[str, Any]:
        pass
