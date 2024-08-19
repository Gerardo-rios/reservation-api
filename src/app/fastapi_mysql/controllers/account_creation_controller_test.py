import uuid
from typing import Any, Dict
from unittest import mock

import pytest
from pytest import MonkeyPatch

from src.domain import Person
from src.interactor.dtos import CreateAccountInputDto, GetRoleInputDto

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
        "src.app.fastapi_mysql.controllers.account_creation_controller.RolMySQLRepository"  # noqa
    )
    mock_account_repository = mocker.patch(
        "src.app.fastapi_mysql.controllers.account_creation_controller.AccountMySQLRepository"  # noqa
    )
    mock_role_presenter = mocker.patch(
        "src.app.fastapi_mysql.controllers.account_creation_controller.GetRolePresenter"  # noqa
    )
    mock_account_presenter = mocker.patch(
        "src.app.fastapi_mysql.controllers.account_creation_controller.CreateAccountPresenter"  # noqa
    )
    mock_get_role_use_case = mocker.patch(
        "src.app.fastapi_mysql.controllers.account_creation_controller.GetRoleUseCase"  # noqa
    )
    mock_create_account_use_case = mocker.patch(
        "src.app.fastapi_mysql.controllers.account_creation_controller.CreateAccountUseCase"  # noqa
    )
    mock_get_role_use_case_instance = mock_get_role_use_case.return_value
    mock_create_account_use_case_instance = mock_create_account_use_case.return_value

    expected_role_use_case_result = {
        "role_id": fixture_role_data["role_id"],
        "role_name": fixture_role_data["role_name"],
        "description": fixture_role_data["description"],
    }

    expected_account_use_case_result = {
        "account_id": fixture_account_data["account_id"],
        "email": fixture_account_data["email"],
        "person_id": "fa360eeb-f000-4fca-a737-71b239d88b5e",
        "person_name": fixture_person_data["name"],
        "role_id": fixture_role_data["role_id"],
        "message": "Account created successfully",
    }

    mock_get_role_use_case_instance.execute.return_value = expected_role_use_case_result
    mock_create_account_use_case_instance.execute.return_value = (
        expected_account_use_case_result
    )

    return {
        "fake_user_inputs": fake_user_inputs,
        "mock_role_repository": mock_role_repository,
        "mock_account_repository": mock_account_repository,
        "mock_role_presenter": mock_role_presenter,
        "mock_account_presenter": mock_account_presenter,
        "mock_get_role_use_case": mock_get_role_use_case,
        "mock_create_account_use_case": mock_create_account_use_case,
        "mock_get_role_use_case_instance": mock_get_role_use_case_instance,
        "mock_create_account_use_case_instance": mock_create_account_use_case_instance,
        "expected_account_use_case_result": expected_account_use_case_result,
    }


def test_create_account(
    test_setup: Dict[str, Any],
    fixture_account_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
) -> None:
    fake_user_inputs = test_setup["fake_user_inputs"]
    mock_role_repository = test_setup["mock_role_repository"]
    mock_account_repository = test_setup["mock_account_repository"]
    mock_role_presenter = test_setup["mock_role_presenter"]
    mock_account_presenter = test_setup["mock_account_presenter"]
    mock_get_role_use_case = test_setup["mock_get_role_use_case"]
    mock_create_account_use_case = test_setup["mock_create_account_use_case"]
    mock_get_role_use_case_instance = test_setup["mock_get_role_use_case_instance"]
    mock_create_account_use_case_instance = test_setup[
        "mock_create_account_use_case_instance"
    ]
    expected_account_use_case_result = test_setup["expected_account_use_case_result"]
    account_input_dto = CreateAccountInputDto(
        email=fixture_account_data["email"],
        password=fixture_account_data["password"],
        user=fixture_account_data["user"],
        photo=fixture_account_data["photo"],
        role_id=fixture_role_data["role_id"],
        person=Person(
            person_id="fa360eeb-f000-4fca-a737-71b239d88b5e", **fixture_person_data
        ),
    )

    role_input_dto = GetRoleInputDto(role_name=fixture_role_data["role_name"])

    controller = CreateAccountController()
    controller.create_request_data(fake_user_inputs)
    result = controller.execute()

    mock_role_repository.assert_called_once()
    mock_account_repository.assert_called_once()
    mock_role_presenter.assert_called_once()
    mock_account_presenter.assert_called_once()
    mock_get_role_use_case.assert_called_once_with(
        role_repository=mock_role_repository.return_value,
        role_presenter=mock_role_presenter.return_value,
    )
    mock_create_account_use_case.assert_called_once_with(
        account_repository=mock_account_repository.return_value,
        presenter=mock_account_presenter.return_value,
    )
    mock_create_account_use_case_instance.execute.assert_called_once_with(
        account_input_dto
    )
    mock_get_role_use_case_instance.execute.assert_called_once_with(role_input_dto)
    assert result == expected_account_use_case_result


def test_create_account__when_some_inputs_are_missing(
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
