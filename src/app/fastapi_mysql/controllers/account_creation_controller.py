from typing import Any, Dict
from src.interactor import (
    CreateAccountUseCase,
    CreatePersonUseCase,
    CreateAccountInputDto,
    CreatePersonInputDto,
)
from src.infra import AccountMySQLRepository, PersonMySQLRepository, RolMySQLRepository
from src.app.fastapi_mysql import (
    AccountControllerInterface,
    CreateAccountPresenter,
    CreatePersonPresenter,
)


class CreateAccountController(AccountControllerInterface):
    def __init__(self) -> None:
        self.input_account_dto: CreateAccountInputDto
        self.input_person_dto: CreatePersonInputDto

    def create_account_info(self, json_input_data: Dict[str, Any]) -> None:
        if not json_input_data:
            raise ValueError("Invalid input data")

        self.input_person_dto = CreatePersonInputDto(
            name=json_input_data["name"],
            phone=json_input_data["phone"],
            address=json_input_data["address"],
            city="loja",
            country="ecuador",
        )

        person_repository = PersonMySQLRepository()
        rol_repository = RolMySQLRepository()
        create_person_use_case = CreatePersonUseCase(
            person_repository=person_repository,
            presenter=CreatePersonPresenter(),
        )

        try:
            person = create_person_use_case.execute(self.input_person_dto)
            role = rol_repository.get(role_name=json_input_data["rol"])
            if not role:
                raise ValueError("Role not found")
            self.input_account_dto = CreateAccountInputDto(
                email=json_input_data["email"],
                password=json_input_data["password"],
                user=json_input_data["user"],
                photo=json_input_data["photo"],
                rol_id=role.rol_id,
                person_id=person["person_id"],
            )
        except Exception as e:
            raise ValueError(f"Person could not be created: {str(e)}")

    def execute(self) -> Dict[str, Any]:
        account_repository = AccountMySQLRepository()
        create_account_use_case = CreateAccountUseCase(
            account_repository=account_repository,
            presenter=CreateAccountPresenter(),
        )

        try:
            response = create_account_use_case.execute(self.input_account_dto)
            return response
        except Exception as e:
            raise ValueError(f"Account could not be created: {str(e)}")
