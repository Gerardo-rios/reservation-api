from typing import Any, Dict, Optional

from src.interactor.interfaces import LoginPresenterInterface
from src.interactor.request_models import LoginOutputDto


class LoginAccountPresenter(LoginPresenterInterface):
    def present(
        self, response: LoginOutputDto, token: Optional[str] = None
    ) -> Dict[str, Any]:
        return {
            "token": token,
            "account": response.account,
        }
