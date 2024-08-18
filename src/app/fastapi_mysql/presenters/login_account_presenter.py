from typing import Any, Dict

from src.interactor.dtos import LoginOutputDto
from src.interactor.interfaces import LoginPresenterInterface


class LoginAccountPresenter(LoginPresenterInterface):
    def present(self, response: LoginOutputDto) -> Dict[str, Any]:
        return {
            "token": response.token,
            "email": response.email,
            "photo": response.photo,
            "user": response.user,
            "name": response.name,
            "phone": response.phone,
            "address": response.address,
            "role": response.role,
        }
