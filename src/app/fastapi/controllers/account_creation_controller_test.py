import uuid
from typing import Any, Dict
from unittest import mock

import pytest
from pytest import MonkeyPatch

from src.interactor import request_models, response_models

with mock.patch(
    "sqlalchemy.create_engine",
) as mock_create_engine:
    from . import CreateAccountController


@pytest.fixture
def test_setup(
    monkeypatch: MonkeyPatch,
    mocker: mock.Mock,
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> Dict[str, Any]:
    del fixture_person_data["person_id"]
    mock_uuid = mocker.patch("uuid.uuid4")
    mock_uuid.return_value = uuid.UUID("fa360eeb-f000-4fca-a737-71b239d88b5e")

    fake_user_inputs = {
        "name": fixture_person_data["name"],
        "phone": fixture_person_data["phone"],
        "address": fixture_person_data["address"],
        "email": fixture_account_data["email"],
        "password": fixture_account_data["password"],
        "user": fixture_account_data["user"],
        "photo": fixture_account_data["photo"],
        "role_name": fixture_role_data["role_name"],
    }

    monkeypatch.setattr("builtins.input", lambda _: next(fake_user_inputs))  # type: ignore  # noqa

    mock_role_repository = mocker.patch(
        "src.app.fastapi.controllers.account_creation_controller.repositories.RolMySQLRepository"  # noqa
    )
    mock_account_repository = mocker.patch(
        "src.app.fastapi.controllers.account_creation_controller.repositories.AccountMySQLRepository"  # noqa
    )
    mock_get_role_use_case = mocker.patch(
        "src.app.fastapi.controllers.account_creation_controller.use_cases.GetRoleUseCase"  # noqa
    )
    mock_create_account_use_case = mocker.patch(
        "src.app.fastapi.controllers.account_creation_controller.use_cases.CreateAccountUseCase"  # noqa
    )
    mock_person_repository = mocker.patch(
        "src.app.fastapi.controllers.account_creation_controller.repositories.PersonMySQLRepository"  # noqa
    )
    mock_create_person_use_case = mocker.patch(
        "src.app.fastapi.controllers.account_creation_controller.use_cases.CreatePersonUseCase"  # noqa
    )
    mock_get_person_use_case = mocker.patch(
        "src.app.fastapi.controllers.account_creation_controller.use_cases.GetPersonUseCase"  # noqa
    )
    mock_get_role_use_case_instance = mock_get_role_use_case.return_value
    mock_create_account_use_case_instance = mock_create_account_use_case.return_value
    mock_create_person_use_case_instance = mock_create_person_use_case.return_value
    mock_get_person_use_case_instance = mock_get_person_use_case.return_value

    expected_role_use_case_result = response_models.GetRoleResponse(
        role_id=fixture_role_data["role_id"],
        role_name=fixture_role_data["role_name"],
        description=fixture_role_data["description"],
    )

    expected_create_person_use_case_result = response_models.CreatePersonResponse(
        person_id="fa360eeb-f000-4fca-a737-71b239d88b5e"
    )

    expected_get_person_use_case_result = response_models.GetPersonResponse(
        person_id="fa360eeb-f000-4fca-a737-71b239d88b5e",
        name=fixture_person_data["name"],
        phone=fixture_person_data["phone"],
        address=fixture_person_data["address"],
        city=fixture_person_data["city"],
        country=fixture_person_data["country"],
    )

    expected_account_use_case_result = {
        "account_id": fixture_account_data["account_id"],
        "person_id": "fa360eeb-f000-4fca-a737-71b239d88b5e",
        "role_id": fixture_role_data["role_id"],
    }

    mock_get_role_use_case_instance.execute.return_value = expected_role_use_case_result
    mock_create_person_use_case_instance.execute.return_value = (
        expected_create_person_use_case_result
    )
    mock_get_person_use_case_instance.execute.return_value = (
        expected_get_person_use_case_result
    )
    mock_create_account_use_case_instance.execute.return_value = (
        expected_account_use_case_result
    )

    return {
        "fake_user_inputs": fake_user_inputs,
        "mock_role_repository": mock_role_repository,
        "mock_account_repository": mock_account_repository,
        "mock_get_role_use_case": mock_get_role_use_case,
        "mock_create_account_use_case": mock_create_account_use_case,
        "mock_get_role_use_case_instance": mock_get_role_use_case_instance,
        "mock_create_account_use_case_instance": mock_create_account_use_case_instance,
        "expected_account_use_case_result": expected_account_use_case_result,
        "mock_person_repository": mock_person_repository,
        "mock_create_person_use_case": mock_create_person_use_case,
        "mock_get_person_use_case": mock_get_person_use_case,
        "mock_create_person_use_case_instance": mock_create_person_use_case_instance,
        "mock_get_person_use_case_instance": mock_get_person_use_case_instance,
    }


def test__create_account_controller__creates_an_account__when_person_is_created_and_input_is_valid(  # noqa
    test_setup: Dict[str, Any],
    fixture_account_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
) -> None:
    fake_user_inputs = test_setup["fake_user_inputs"]
    mock_role_repository = test_setup["mock_role_repository"]
    mock_account_repository = test_setup["mock_account_repository"]
    mock_get_role_use_case = test_setup["mock_get_role_use_case"]
    mock_create_account_use_case = test_setup["mock_create_account_use_case"]
    mock_get_role_use_case_instance = test_setup["mock_get_role_use_case_instance"]
    mock_person_repository = test_setup["mock_person_repository"]
    mock_create_person_use_case = test_setup["mock_create_person_use_case"]
    mock_create_account_use_case_instance = test_setup[
        "mock_create_account_use_case_instance"
    ]
    expected_account_use_case_result = test_setup["expected_account_use_case_result"]
    account_request_input = request_models.CreateAccountRequest(
        email=fixture_account_data["email"],
        password=fixture_account_data["password"],
        user=fixture_account_data["user"],
        photo=fixture_account_data["photo"],
        role_id=fixture_role_data["role_id"],
        person_id="fa360eeb-f000-4fca-a737-71b239d88b5e",
    )

    role_request_input = request_models.GetRoleRequest(
        role_name=fixture_role_data["role_name"]
    )

    controller = CreateAccountController()
    controller.create_request_data(fake_user_inputs)
    response = controller.execute()

    mock_role_repository.assert_called_once()
    mock_person_repository.assert_called_once()
    mock_account_repository.assert_called_once()
    mock_get_role_use_case.assert_called_once_with(
        role_repository=mock_role_repository.return_value,
    )
    mock_create_person_use_case.assert_called_once_with(
        person_repository=mock_person_repository.return_value,
    )
    mock_create_account_use_case.assert_called_once_with(
        account_repository=mock_account_repository.return_value,
    )
    mock_create_account_use_case_instance.execute.assert_called_once_with(
        account_request_input
    )
    mock_get_role_use_case_instance.execute.assert_called_once_with(role_request_input)
    assert response == expected_account_use_case_result


def test__create_account_controller__creates_an_account__when_person_is_already_created_and_input_is_valid(  # noqa
    test_setup: Dict[str, Any],
    fixture_account_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
) -> None:
    fake_user_inputs = test_setup["fake_user_inputs"]
    mock_role_repository = test_setup["mock_role_repository"]
    mock_account_repository = test_setup["mock_account_repository"]
    mock_get_role_use_case = test_setup["mock_get_role_use_case"]
    mock_create_account_use_case = test_setup["mock_create_account_use_case"]
    mock_get_role_use_case_instance = test_setup["mock_get_role_use_case_instance"]
    mock_person_repository = test_setup["mock_person_repository"]
    mock_create_person_use_case = test_setup["mock_create_person_use_case"]
    mock_create_person_use_case_instance = test_setup[
        "mock_create_person_use_case_instance"
    ]
    mock_get_person_use_case = test_setup["mock_get_person_use_case"]
    mock_get_person_use_case_instance = test_setup["mock_get_person_use_case_instance"]
    mock_create_account_use_case_instance = test_setup[
        "mock_create_account_use_case_instance"
    ]
    expected_account_use_case_result = test_setup["expected_account_use_case_result"]
    mock_create_person_use_case_instance.execute.return_value = None
    account_request_input = request_models.CreateAccountRequest(
        email=fixture_account_data["email"],
        password=fixture_account_data["password"],
        user=fixture_account_data["user"],
        photo=fixture_account_data["photo"],
        role_id=fixture_role_data["role_id"],
        person_id="fa360eeb-f000-4fca-a737-71b239d88b5e",
    )

    role_request_input = request_models.GetRoleRequest(
        role_name=fixture_role_data["role_name"]
    )

    controller = CreateAccountController()
    controller.create_request_data(fake_user_inputs)
    response = controller.execute()

    mock_role_repository.assert_called_once()
    mock_person_repository.assert_called_once()
    mock_account_repository.assert_called_once()
    mock_get_role_use_case.assert_called_once_with(
        role_repository=mock_role_repository.return_value,
    )
    mock_create_person_use_case.assert_called_once_with(
        person_repository=mock_person_repository.return_value,
    )
    mock_get_person_use_case.assert_called_once_with(
        person_repository=mock_person_repository.return_value,
    )
    mock_create_account_use_case.assert_called_once_with(
        account_repository=mock_account_repository.return_value,
    )
    mock_create_account_use_case_instance.execute.assert_called_once_with(
        account_request_input
    )
    mock_get_role_use_case_instance.execute.assert_called_once_with(role_request_input)
    mock_get_person_use_case_instance.execute.assert_called_once()
    assert response == expected_account_use_case_result


def test__create_account_controller__raises_error__with_missing_input_fields(
    test_setup: Dict[str, Any],
    fixture_account_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
) -> None:
    fake_user_inputs = test_setup["fake_user_inputs"]

    controller = CreateAccountController()
    fake_user_inputs.pop("name")
    with pytest.raises(ValueError) as exc_info:
        controller.create_request_data(fake_user_inputs)
    assert str(exc_info.value) == "Missing keys: name"

    fake_user_inputs["name"] = fixture_person_data["name"]
    fake_user_inputs.pop("role_name")
    with pytest.raises(ValueError) as exc_info:
        controller.create_request_data(fake_user_inputs)
    assert str(exc_info.value) == "Missing keys: role_name"

    fake_user_inputs["role_name"] = fixture_role_data["role_name"]
    fake_user_inputs.pop("email")
    with pytest.raises(ValueError) as exc_info:
        controller.create_request_data(fake_user_inputs)
    assert str(exc_info.value) == "Missing keys: email"

    fake_user_inputs["email"] = fixture_account_data["email"]
    fake_user_inputs.pop("password")
    with pytest.raises(ValueError) as exc_info:
        controller.create_request_data(fake_user_inputs)
    assert str(exc_info.value) == "Missing keys: password"


def test__create_account_controller__raises_an_error_when_a_person_was_not_found_and_could_not_be_created(  # noqa
    test_setup: Dict[str, Any]
) -> None:
    fake_user_inputs = test_setup["fake_user_inputs"]
    mock_create_person_use_case_instance = test_setup[
        "mock_create_person_use_case_instance"
    ]
    mock_get_person_use_case_instance = test_setup["mock_get_person_use_case_instance"]
    mock_create_person_use_case_instance.execute.return_value = None
    mock_get_person_use_case_instance.execute.return_value = None

    controller = CreateAccountController()

    with pytest.raises(ValueError) as exc_info:
        controller.create_request_data(fake_user_inputs)
        controller.execute()
    assert str(exc_info.value) == "An error occurred while creating person"
