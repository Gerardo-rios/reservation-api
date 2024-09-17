from typing import Any, Dict, Optional

from src.domain.interfaces import LoginPresenterInterface
from src.domain.request_models import LoginOutputDto


class LoginAccountPresenter(LoginPresenterInterface):
    def present(
        self, output_dto: LoginOutputDto, token: Optional[str] = None
    ) -> Dict[str, Any]:
        return {
            "token": token,
            "account": output_dto.account,
        }
