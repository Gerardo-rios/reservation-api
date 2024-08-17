import uuid
from typing import Any, Dict

from src.app.fastapi_mysql.interfaces import AccountControllerInterface
from src.app.fastapi_mysql.presenters import CreateAccountPresenter, GetRolePresenter
from src.domain import Person
from src.infra import AccountMySQLRepository, RolMySQLRepository
from src.interactor.dtos import CreateAccountInputDto, GetRoleInputDto
from src.interactor.use_cases import CreateAccountUseCase, GetRoleUseCase


class CreateAccountController(AccountControllerInterface):
    def __init__(self) -> None:
        self.input_account_dto: CreateAccountInputDto

    def create_account_request_data(self, json_input_data: Dict[str, Any]) -> None:
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
        input_keys = set(json_input_data.keys())
        valid_keys_set = set(valid_keys)

        missing_keys = valid_keys_set - input_keys
        invalid_keys = input_keys - valid_keys_set

        if missing_keys or invalid_keys:
            error_message = []
            if missing_keys:
                error_message.append(f"Missing keys: {', '.join(missing_keys)}")
            if invalid_keys:
                error_message.append(f"Invalid keys: {', '.join(invalid_keys)}")

            raise ValueError(". ".join(error_message))

        role_repository = RolMySQLRepository()
        get_role_use_case = GetRoleUseCase(
            role_repository=role_repository,
            role_presenter=GetRolePresenter(),
        )
        role = get_role_use_case.execute(
            GetRoleInputDto(role_name=json_input_data["role_name"])
        )
        if not role:
            raise ValueError("Role not found")

        self.input_account_dto = CreateAccountInputDto(
            email=json_input_data["email"],
            password=json_input_data["password"],
            user=json_input_data["user"],
            photo=json_input_data["photo"],
            role_id=role["role_id"],
            person=Person(
                person_id=str(uuid.uuid4()),
                name=json_input_data["name"],
                phone=json_input_data["phone"],
                address=json_input_data["address"],
                city="loja",
                country="ecuador",
            ),
        )

    def execute(self) -> Dict[str, Any]:
        repository = AccountMySQLRepository()
        presenter = CreateAccountPresenter()
        use_case = CreateAccountUseCase(
            account_repository=repository,
            presenter=presenter,
        )
        result = use_case.execute(self.input_account_dto)
        return result
