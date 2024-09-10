from typing import Any, Dict

from src.interactor.interfaces import LoginPresenterInterface
from src.interactor.request_models import LoginOutputDto


class LoginAccountPresenter(LoginPresenterInterface):
    def present(self, response: LoginOutputDto) -> Dict[str, Any]:
        return {
            "token": response.token,
            "session": response.session.to_dict(),
        }
