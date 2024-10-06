from typing import Any, Dict

from src.app.fastapi import interfaces
from src.infra import repositories
from src.interactor import request_models, use_cases

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

    # TODO: Add types to the return
    def execute(self) -> Dict[str, Any]:
        account_repository = repositories.AccountMySQLRepository()
        account_use_case = use_cases.GetAccountUseCase(
            account_repository=account_repository
        )
        account = account_use_case.execute(request_input=self.get_account_request)
        person_repository = repositories.PersonMySQLRepository()
        person_use_case = use_cases.GetPersonUseCase(
            person_repository=person_repository
        )
        person = person_use_case.execute(
            request_input=request_models.GetPersonRequest(person_id=account.person_id)
        )
        role_repository = repositories.RolMySQLRepository()
        role_use_case = use_cases.GetRoleUseCase(role_repository=role_repository)
        role = role_use_case.execute(
            request_input=request_models.GetRoleRequest(role_id=account.role_id)
        )

        # TODO: Not include the password in the response
        response = {"account": account.account, "person": person, "role": role}

        return response
