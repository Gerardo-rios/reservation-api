from typing import Any, Dict
from src.interactor import CreateAccountOutputDto, CreateAccountPresenterInterface


class CreateAccountPresenter(CreateAccountPresenterInterface):
    def present(self, response: CreateAccountOutputDto) -> Dict[str, Any]:
        return {
            "account_id": response.account.account_id,
            "email": response.account.email,
            "user": response.account.user,
            "photo": response.account.photo,
            "status": response.account.status,
            "person_id": response.person_id,
            "role_id": response.role_id,
        }
