from typing import Any, Dict
from src.interactor import CreateAccountOutputDto, CreateAccountPresenterInterface


class CreateAccountPresenter(CreateAccountPresenterInterface):
    def present(self, response: CreateAccountOutputDto) -> Dict[str, Any]:
        return {
            "account_id": response.account.account_id,
            "email": response.account.email,
            "person_id": response.person.person_id,
            "person_name": response.person.name,
            "role_id": response.role_id,
            "message": "Account created successfully",
        }
