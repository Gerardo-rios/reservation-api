from typing import Any, Dict
from unittest import mock

import jwt
import pytest
from pytest import MonkeyPatch

from src.interactor import request_models

with mock.patch(
    "sqlalchemy.create_engine",
) as mock_create_engine:
    from . import LoginAccountController


@pytest.fixture
def test_setup(
    monkeypatch: MonkeyPatch,
    mocker: mock.Mock,
    fixture_account_data: Dict[str, Any],
) -> Dict[str, Any]:
    fake_user_inputs = {
        "email": fixture_account_data["email"],
        "password": fixture_account_data["password"],
    }

    monkeypatch.setattr("builtins.input", lambda _: next(fake_user_inputs))  # type: ignore  # noqa

    mock_login_repository = mocker.patch(
        "src.app.fastapi.controllers.login_account_controller.repositories.LoginMySQLRepository"  # noqa
    )
    mock_login_use_case = mocker.patch(
        "src.app.fastapi.controllers.login_account_controller.use_cases.LoginUseCase"  # noqa
    )
    mock_login_use_case_instance = mock_login_use_case.return_value

    monkeypatch.setattr(jwt, "encode", lambda payload, secret, algorithm: "test_token")

    expected_login_use_case_response = {
        "token": "test_token",
        "account": fixture_account_data["account_id"],
    }

    mock_login_use_case_instance.execute.return_value = expected_login_use_case_response

    return {
        "fake_user_inputs": fake_user_inputs,
        "mock_login_repository": mock_login_repository,
        "mock_login_use_case": mock_login_use_case,
        "mock_login_use_case_instance": mock_login_use_case_instance,
        "expected_login_use_case_response": expected_login_use_case_response,
        "account_data": fixture_account_data,
    }


def test__login__returns__an_auth_token_and_account_id__when_successful(
    test_setup: Dict[str, Any]
) -> None:
    fake_user_inputs = test_setup["fake_user_inputs"]
    mock_login_repository = test_setup["mock_login_repository"]
    mock_login_use_case = test_setup["mock_login_use_case"]
    mock_login_use_case_instance = test_setup["mock_login_use_case_instance"]
    expected_login_use_case_response = test_setup["expected_login_use_case_response"]

    login_input_dto = request_models.LoginRequest(
        email=test_setup["account_data"]["email"],
        password=test_setup["account_data"]["password"],
    )
    controller = LoginAccountController()
    controller.create_request_data(fake_user_inputs)
    result = controller.execute()

    mock_login_repository.assert_called_once()
    mock_login_use_case.assert_called_once_with(
        login_repository=mock_login_repository.return_value,
    )
    mock_login_use_case_instance.execute.assert_called_once_with(
        request_input=login_input_dto, auth_token="test_token"
    )
    assert result == expected_login_use_case_response


def test__login_account__raises_value_errors__when_some_inputs_are_missing(
    test_setup: Dict[str, Any]
) -> None:
    fake_user_inputs = test_setup["fake_user_inputs"]
    controller = LoginAccountController()
    fake_user_inputs.pop("email")

    with pytest.raises(ValueError) as exc_info:
        controller.create_request_data(fake_user_inputs)
    assert str(exc_info.value) == "Missing keys: email"

    fake_user_inputs["email"] = test_setup["account_data"]["email"]
    fake_user_inputs.pop("password")

    with pytest.raises(ValueError) as exc_info:
        controller.create_request_data(fake_user_inputs)
    assert str(exc_info.value) == "Missing keys: password"
