from typing import Any, Dict

from src.interactor.dtos import LoginOutputDto
from src.interactor.interfaces import LoginPresenterInterface


class LoginAccountPresenter(LoginPresenterInterface):
    def present(self, response: LoginOutputDto) -> Dict[str, Any]:
        return {
            "token": response.token,
            "session": response.session.to_dict(),
        }
