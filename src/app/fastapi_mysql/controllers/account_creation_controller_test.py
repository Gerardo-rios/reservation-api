import pytest
from unittest.mock import Mock, patch
from src.app.fastapi_mysql.controllers import CreateAccountController
from src.interactor import CreatePersonUseCase, GetRoleUseCase, CreateAccountUseCase


@pytest.fixture
def create_account_controller() -> CreateAccountController:
    return CreateAccountController()


def test_create_account_info_valid_input(
    create_account_controller: CreateAccountController,
) -> None:
    valid_input = {
        "name": "John Doe",
        "phone": "1234567890",
        "address": "123 Main St",
        "email": "john@example.com",
        "password": "Str0ngpassword!23",
        "user": "johndoe",
        "photo": "profile.jpg",
        "role_name": "user",
    }

    with patch.object(
        CreatePersonUseCase,
        "execute",
        return_value={"person_id": "033f9886-316a-401b-9414-78c57f4ac502"},
    ), patch.object(
        GetRoleUseCase,
        "execute",
        return_value={"role_id": "1b4c1948-3cb3-46d1-85c6-454a457216aa"},
    ):
        create_account_controller.create_account_info(valid_input)

    assert create_account_controller.input_person_dto.name == "John Doe"
    assert create_account_controller.input_person_dto.phone == "1234567890"
    assert create_account_controller.input_person_dto.address == "123 Main St"
    assert create_account_controller.input_person_dto.city == "loja"
    assert create_account_controller.input_person_dto.country == "ecuador"

    assert create_account_controller.input_account_dto.email == "john@example.com"
    assert create_account_controller.input_account_dto.password == "Str0ngpassword!23"
    assert create_account_controller.input_account_dto.user == "johndoe"
    assert create_account_controller.input_account_dto.photo == "profile.jpg"
    assert (
        create_account_controller.input_account_dto.role_id
        == "1b4c1948-3cb3-46d1-85c6-454a457216aa"
    )
    assert (
        create_account_controller.input_account_dto.person_id
        == "033f9886-316a-401b-9414-78c57f4ac502"
    )


def test_create_account_info_invalid_input(
    create_account_controller: CreateAccountController,
) -> None:
    with pytest.raises(ValueError, match="Invalid input data"):
        create_account_controller.create_account_info({})


def test_create_account_info_person_creation_failure(
    create_account_controller: CreateAccountController,
) -> None:
    valid_input = {
        "name": "John Doe",
        "phone": "1234567890",
        "address": "123 Main St",
        "email": "john@example.com",
        "password": "password123",
        "user": "johndoe",
        "photo": "profile.jpg",
    }

    with patch.object(
        CreatePersonUseCase, "execute", side_effect=Exception("Person creation failed")
    ):
        with pytest.raises(
            ValueError, match="Person could not be created: Person creation failed"
        ):
            create_account_controller.create_account_info(valid_input)


def test_create_account_info_role_not_found(
    create_account_controller: CreateAccountController,
) -> None:
    valid_input = {
        "name": "John Doe",
        "phone": "1234567890",
        "address": "123 Main St",
        "email": "john@example.com",
        "password": "password123",
        "user": "johndoe",
        "photo": "profile.jpg",
    }

    with patch.object(
        CreatePersonUseCase, "execute", return_value={"person_id": 1}
    ), patch.object(GetRoleUseCase, "execute", return_value=None):
        with pytest.raises(ValueError, match="Role not found"):
            create_account_controller.create_account_info(valid_input)


def test_execute_successful(create_account_controller: CreateAccountController) -> None:
    create_account_controller.input_account_dto = Mock()
    expected_response = {"account_id": 1, "message": "Account created successfully"}

    with patch.object(CreateAccountUseCase, "execute", return_value=expected_response):
        response = create_account_controller.execute()

    assert response == expected_response


def test_execute_failure(create_account_controller: CreateAccountController) -> None:
    create_account_controller.input_account_dto = Mock()

    with patch.object(
        CreateAccountUseCase,
        "execute",
        side_effect=Exception("Account creation failed"),
    ):
        with pytest.raises(
            ValueError, match="Account could not be created: Account creation failed"
        ):
            create_account_controller.execute()
