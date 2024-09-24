from typing import Any, Dict

from src.app.fastapi import interfaces
from src.infra import repositories
from src.interactor import request_models, response_models, use_cases

from . import controllers_utils


class CreateAccountController(interfaces.AccountControllerInterface):
    def __init__(self) -> None:
        self.input_account_request: request_models.CreateAccountRequest

    def create_request_data(self, json_input_data: Dict[str, Any]) -> None:
        valid_keys = [
            "name",
            "phone",
            "address",
            "role_name",
            "email",
            "password",
            "user",
            "photo",
        ]
        controllers_utils.validate_input_keys(json_input_data, valid_keys)

        role_repository = repositories.RolMySQLRepository()
        get_role_use_case = use_cases.GetRoleUseCase(role_repository=role_repository)
        role = get_role_use_case.execute(
            request_models.GetRoleRequest(role_name=json_input_data["role_name"])
        )
        if not role:
            raise ValueError("Role not found")

        person_repository = repositories.PersonMySQLRepository()
        create_person_use_case = use_cases.CreatePersonUseCase(
            person_repository=person_repository
        )
        get_person_use_case = use_cases.GetPersonUseCase(
            person_repository=person_repository
        )
        person = create_person_use_case.execute()
        if not person:
            person = get_person_use_case.execute()

        self.input_account_request = request_models.CreateAccountRequest(
            email=json_input_data["email"],
            password=json_input_data["password"],
            user=json_input_data["user"],
            photo=json_input_data["photo"],
            role_id=role.role_id,
            person_id=person["person_id"],
        )

    def execute(self) -> response_models.CreateAccountResponse:
        repository = repositories.AccountMySQLRepository()
        use_case = use_cases.CreateAccountUseCase(account_repository=repository)
        response = use_case.execute(self.input_account_request)
        return response
