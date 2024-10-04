from typing import Any, Dict

from src.app.fastapi import interfaces
from src.infra import repositories
from src.interactor import request_models, response_models, use_cases

from . import controllers_utils


class GetAccountDataController(interfaces.GetAccountControllerInterface):
    def __init__(self) -> None:
        self.get_account_request: request_models.GetAccountByIdRequest

    def create_request_data(self, json_input_data: Dict[str, Any]) -> None:
        valid_keys = ["account_id"]
        controllers_utils.validate_input_keys(json_input_data, valid_keys)

        self.get_account_request = request_models.GetAccountByIdRequest(
            account_id=json_input_data["account_id"]
        )

    def execute(self) -> response_models.GetAccountResponse:
        repository = repositories.AccountMySQLRepository()
        use_case = use_cases.GetAccountUseCase(account_repository=repository)
        response = use_case.execute(request_input=self.get_account_request)
        return response
