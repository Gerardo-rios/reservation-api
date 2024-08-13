from typing import Dict
import pytest
from unittest.mock import patch, MagicMock
from src.app.fastapi_mysql import CreateAccountController
from src.interactor import CreateAccountInputDto, CreatePersonInputDto


@pytest.fixture
def valid_input_data() -> Dict[str, str]:
    return {
        "name": "John Doe",
        "phone": "1234567890",
        "address": "123 Main St",
        "email": "john.doe@example.com",
        "password": "S3curep@ssw0rd!",
        "user": "johndoe",
        "photo": "photo_url",
        "rol": "admin",
    }


@pytest.fixture
def invalid_input_data() -> Dict[str, str]:
    return {
        "name": "John Doe",
        "phone": "1234567890",
        "address": "123 Main St",
        "email": "john.doe@example.com",
        "password": "securepassword",
        "user": "johndoe",
        "photo": "photo_url",
    }


@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.PersonMySQLRepository"  # noqa
)
@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.RolMySQLRepository"
)
@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.CreatePersonUseCase"
)
@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.CreatePersonPresenter"  # noqa
)
def test_create_account_info_valid(
    mock_person_presenter: MagicMock,
    mock_person_use_case: MagicMock,
    mock_rol_repo: MagicMock,
    mock_person_repo: MagicMock,
    valid_input_data: Dict[str, str],
) -> None:
    mock_person_use_case.return_value.execute.return_value = {
        "person_id": "d7b25679-4dbd-4c4a-a5ac-d929e230e76f"
    }
    mock_rol_repo.return_value.get.return_value = MagicMock(
        rol_id="5be5c5e2-ba46-4455-9f63-9050b5f6421e"
    )

    controller = CreateAccountController()
    controller.create_account_info(valid_input_data)

    assert isinstance(controller.input_person_dto, CreatePersonInputDto)
    assert isinstance(controller.input_account_dto, CreateAccountInputDto)


@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.PersonMySQLRepository"  # noqa
)
@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.RolMySQLRepository"
)
@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.CreatePersonUseCase"
)
@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.CreatePersonPresenter"  # noqa
)
def test_create_account_info_invalid(
    mock_person_presenter: MagicMock,
    mock_person_use_case: MagicMock,
    mock_rol_repo: MagicMock,
    mock_person_repo: MagicMock,
    invalid_input_data: Dict[str, str],
) -> None:
    controller = CreateAccountController()

    with pytest.raises(ValueError):
        controller.create_account_info(invalid_input_data)


@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.AccountMySQLRepository"  # noqa
)
@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.CreateAccountUseCase"
)
@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.CreateAccountPresenter"  # noqa
)
def test_execute_success(
    mock_account_presenter: MagicMock,
    mock_account_use_case: MagicMock,
    mock_account_repo: MagicMock,
    valid_input_data: Dict[str, str],
) -> None:
    mock_account_use_case.return_value.execute.return_value = {
        "account_id": "e537c036-4ac4-45ef-b7df-0e3c585483d7"
    }

    controller = CreateAccountController()
    controller.input_account_dto = CreateAccountInputDto(
        email=valid_input_data["email"],
        password=valid_input_data["password"],
        user=valid_input_data["user"],
        photo=valid_input_data["photo"],
        rol_id="5be5c5e2-ba46-4455-9f63-9050b5f6421e",
        person_id="d7b25679-4dbd-4c4a-a5ac-d929e230e76f",
    )

    response = controller.execute()

    assert response == {"account_id": "e537c036-4ac4-45ef-b7df-0e3c585483d7"}


@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.AccountMySQLRepository"  # noqa
)
@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.CreateAccountUseCase"
)
@patch(
    "src.app.fastapi_mysql.controllers.account_creation_controller.CreateAccountPresenter"  # noqa
)
def test_execute_failure(
    mock_account_presenter: MagicMock,
    mock_account_use_case: MagicMock,
    mock_account_repo: MagicMock,
) -> None:
    mock_account_use_case.return_value.execute.side_effect = Exception(
        "Account creation failed"
    )

    controller = CreateAccountController()
    controller.input_account_dto = MagicMock()

    with pytest.raises(ValueError):
        controller.execute()
