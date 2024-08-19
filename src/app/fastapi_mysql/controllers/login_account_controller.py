from typing import Any, Dict

from src.app.fastapi_mysql.interfaces import AccountControllerInterface
from src.app.fastapi_mysql.presenters import LoginAccountPresenter
from src.infra import LoginMySQLRepository
from src.interactor.dtos import LoginInputDto
from src.interactor.use_cases import LoginUseCase

from .controllers_utils import validate_input_keys


class LoginAccountController(AccountControllerInterface):
    def __init__(self) -> None:
        self.input_login_dto: LoginInputDto

    def create_request_data(self, json_input_data: Dict[str, Any]) -> None:
        valid_keys = ["email", "password"]
        validate_input_keys(json_input_data, valid_keys)

        self.input_login_dto = LoginInputDto(
            email=json_input_data["email"], password=json_input_data["password"]
        )

    def execute(self) -> Dict[str, Any]:
        repository = LoginMySQLRepository()
        presenter = LoginAccountPresenter()
        use_case = LoginUseCase(
            login_repository=repository,
            login_presenter=presenter,
        )
        result = use_case.execute(self.input_login_dto)
        return result
