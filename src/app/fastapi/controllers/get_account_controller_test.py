from typing import Any, Dict
from unittest import mock

import pytest
from pytest import MonkeyPatch

from src.domain import entities
from src.interactor import request_models, response_models

with mock.patch(
    "sqlalchemy.create_engine",
) as mock_create_engine:
    from . import GetAccountDataController


@pytest.fixture
def test_setup(
    monkeypatch: MonkeyPatch,
    mocker: mock.Mock,
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> Dict[str, Any]:
    fake_input = {
        "account_id": fixture_account_data["account_id"],
    }

    account = entities.Account(**fixture_account_data)

    monkeypatch.setattr("builtins.input", lambda _: next(fake_input))  # type: ignore

    mock_account_repository = mocker.patch(
        "src.app.fastapi.controllers.get_account_controller.repositories.AccountMySQLRepository"  # noqa
    )
    mock_account_use_case = mocker.patch(
        "src.app.fastapi.controllers.get_account_controller.use_cases.GetAccountUseCase"  # noqa
    )
    mock_account_use_case_instance = mock_account_use_case.return_value

    mock_person_repository = mocker.patch(
        "src.app.fastapi.controllers.get_account_controller.repositories.PersonMySQLRepository"  # noqa
    )
    mock_person_use_case = mocker.patch(
        "src.app.fastapi.controllers.get_account_controller.use_cases.GetPersonUseCase"  # noqa
    )
    mock_person_use_case_instance = mock_person_use_case.return_value

    mock_role_repository = mocker.patch(
        "src.app.fastapi.controllers.get_account_controller.repositories.RolMySQLRepository"  # noqa
    )
    mock_role_use_case = mocker.patch(
        "src.app.fastapi.controllers.get_account_controller.use_cases.GetRoleUseCase"  # noqa
    )
    mock_role_use_case_instance = mock_role_use_case.return_value

    expected_get_account_use_case_response = response_models.GetAccountResponse(
        account=account,
        person_id=fixture_person_data["person_id"],
        role_id=fixture_role_data["role_id"],
    )
    mock_account_use_case_instance.execute.return_value = (
        expected_get_account_use_case_response
    )

    expected_get_person_use_case_response = response_models.GetPersonResponse(
        **fixture_person_data
    )
    mock_person_use_case_instance.execute.return_value = (
        expected_get_person_use_case_response
    )

    expected_get_role_use_case_response = response_models.GetRoleResponse(
        **fixture_role_data
    )
    mock_role_use_case_instance.execute.return_value = (
        expected_get_role_use_case_response
    )

    return {
        "fake_user_inputs": fake_input,
        "mock_account_repository": mock_account_repository,
        "mock_account_use_case": mock_account_use_case,
        "mock_account_use_case_instance": mock_account_use_case_instance,
        "expected_get_account_use_case_response": expected_get_account_use_case_response,  # noqa
        "mock_person_repository": mock_person_repository,
        "mock_person_use_case": mock_person_use_case,
        "mock_person_use_case_instance": mock_person_use_case_instance,
        "expected_get_person_use_case_response": expected_get_person_use_case_response,  # noqa
        "mock_role_repository": mock_role_repository,
        "mock_role_use_case": mock_role_use_case,
        "mock_role_use_case_instance": mock_role_use_case_instance,
        "expected_get_role_use_case_response": expected_get_role_use_case_response,
    }


def test__get_account_controller__returns__an_account_id__when_successful(
    test_setup: Dict[str, Any]
) -> None:
    fake_input = test_setup["fake_user_inputs"]
    mock_account_repository = test_setup["mock_account_repository"]
    mock_account_use_case = test_setup["mock_account_use_case"]
    mock_account_use_case_instance = test_setup["mock_account_use_case_instance"]
    expected_get_account_use_case_response = test_setup[
        "expected_get_account_use_case_response"
    ]
    mock_person_repository = test_setup["mock_person_repository"]
    mock_person_use_case = test_setup["mock_person_use_case"]
    mock_person_use_case_instance = test_setup["mock_person_use_case_instance"]
    expected_get_person_use_case_response = test_setup[
        "expected_get_person_use_case_response"
    ]
    mock_role_repository = test_setup["mock_role_repository"]
    mock_role_use_case = test_setup["mock_role_use_case"]
    mock_role_use_case_instance = test_setup["mock_role_use_case_instance"]
    expected_get_role_use_case_response = test_setup[
        "expected_get_role_use_case_response"
    ]

    get_account_input_dto = request_models.GetAccountByIdRequest(
        account_id=fake_input["account_id"]
    )
    controller = GetAccountDataController()
    controller.create_request_data(fake_input)
    result = controller.execute()

    mock_account_repository.assert_called_once()
    mock_person_repository.assert_called_once()
    mock_role_repository.assert_called_once()
    mock_account_use_case.assert_called_once_with(
        account_repository=mock_account_repository.return_value,
    )
    mock_person_use_case.assert_called_once_with(
        person_repository=mock_person_repository.return_value,
    )
    mock_role_use_case.assert_called_once_with(
        role_repository=mock_role_repository.return_value,
    )
    mock_account_use_case_instance.execute.assert_called_once_with(
        request_input=get_account_input_dto
    )
    mock_person_use_case_instance.execute.assert_called_once_with(
        request_input=request_models.GetPersonRequest(
            person_id=expected_get_account_use_case_response.person_id
        )
    )
    mock_role_use_case_instance.execute.assert_called_once_with(
        request_input=request_models.GetRoleRequest(
            role_id=expected_get_account_use_case_response.role_id
        )
    )

    expected_response = {
        "account": expected_get_account_use_case_response.account,
        "person": expected_get_person_use_case_response,
        "role": expected_get_role_use_case_response,
    }

    assert result == expected_response


def test__get_account__raises_value_errors__when_some_inputs_are_missing(
    test_setup: Dict[str, Any]
) -> None:
    fake_user_inputs = test_setup["fake_user_inputs"]
    controller = GetAccountDataController()
    fake_user_inputs.pop("account_id")

    with pytest.raises(ValueError) as exc_info:
        controller.create_request_data(fake_user_inputs)
    assert str(exc_info.value) == "Missing keys: account_id"
