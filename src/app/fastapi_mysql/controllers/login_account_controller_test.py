from typing import Any, Dict
from unittest import mock

import pytest
from pytest import MonkeyPatch

from src.interactor.dtos import LoginInputDto

with mock.patch(
    "sqlalchemy.create_engine",
) as mock_create_engine:
    from . import LoginAccountController


@pytest.fixture
def test_setup(
    monkeypatch: MonkeyPatch,
    mocker: mock.Mock,
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> Dict[str, Any]:
    fake_user_inputs = {
        "email": fixture_account_data["email"],
        "password": fixture_account_data["password"],
    }

    monkeypatch.setattr("builtins.input", lambda _: next(fake_user_inputs))  # type: ignore  # noqa

    mock_login_repository = mocker.patch(
        "src.app.fastapi_mysql.controllers.login_account_controller.LoginMySQLRepository"  # noqa
    )
    mock_login_presenter = mocker.patch(
        "src.app.fastapi_mysql.controllers.login_account_controller.LoginAccountPresenter"  # noqa
    )
    mock_login_use_case = mocker.patch(
        "src.app.fastapi_mysql.controllers.login_account_controller.LoginUseCase"  # noqa
    )
    mock_login_use_case_instance = mock_login_use_case.return_value

    test_data = {
        "account": fixture_account_data,
        "person": fixture_person_data,
        "role": fixture_role_data,
    }

    expected_login_use_case_response = {
        "token": "test_token",
        "session": {
            "account": {
                "account_id": fixture_account_data["account_id"],
                "email": fixture_account_data["email"],
                "user": fixture_account_data["user"],
                "photo": fixture_account_data["photo"],
            },
            "person": {
                "person_id": fixture_person_data["person_id"],
                "name": fixture_person_data["name"],
                "phone": fixture_person_data["phone"],
                "address": fixture_person_data["address"],
            },
            "role": {
                "role_id": fixture_role_data["role_id"],
                "role_name": fixture_role_data["role_name"],
            },
        },
    }

    mock_login_use_case_instance.execute.return_value = expected_login_use_case_response

    return {
        "fake_user_inputs": fake_user_inputs,
        "mock_login_repository": mock_login_repository,
        "mock_login_presenter": mock_login_presenter,
        "mock_login_use_case": mock_login_use_case,
        "mock_login_use_case_instance": mock_login_use_case_instance,
        "expected_login_use_case_response": expected_login_use_case_response,
        "test_data": test_data,
    }


def test_create_account(test_setup: Dict[str, Any]) -> None:
    fake_user_inputs = test_setup["fake_user_inputs"]
    mock_login_repository = test_setup["mock_login_repository"]
    mock_login_presenter = test_setup["mock_login_presenter"]
    mock_login_use_case = test_setup["mock_login_use_case"]
    mock_login_use_case_instance = test_setup["mock_login_use_case_instance"]
    expected_login_use_case_response = test_setup["expected_login_use_case_response"]
    login_input_dto = LoginInputDto(
        email=test_setup["test_data"]["account"]["email"],
        password=test_setup["test_data"]["account"]["password"],
    )

    controller = LoginAccountController()
    controller.create_request_data(fake_user_inputs)
    result = controller.execute()

    mock_login_repository.assert_called_once()
    mock_login_presenter.assert_called_once()
    mock_login_use_case.assert_called_once_with(
        login_repository=mock_login_repository.return_value,
        login_presenter=mock_login_presenter.return_value,
    )
    mock_login_use_case_instance.execute.assert_called_once_with(login_input_dto)
    assert result == expected_login_use_case_response


def test_create_account__when_some_inputs_are_missing(
    test_setup: Dict[str, Any]
) -> None:
    fake_user_inputs = test_setup["fake_user_inputs"]
    controller = LoginAccountController()
    fake_user_inputs.pop("email")
    with pytest.raises(ValueError) as exc_info:
        controller.create_request_data(fake_user_inputs)
    assert str(exc_info.value) == "Missing keys: email"

    fake_user_inputs["email"] = test_setup["test_data"]["account"]["email"]
    fake_user_inputs.pop("password")
    with pytest.raises(ValueError) as exc_info:
        controller.create_request_data(fake_user_inputs)
    assert str(exc_info.value) == "Missing keys: password"

    fake_user_inputs["password"] = test_setup["test_data"]["account"]["password"]
