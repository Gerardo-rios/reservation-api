from dataclasses import asdict
from typing import Any, Callable, Dict

import pytest
from pytest_mock import MockFixture

from src.domain import entities, interfaces
from src.interactor import errors, request_models, response_models, use_cases


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[[entities.Account], Dict[str, Any]]:
    def _factory(
        account: entities.Account,
    ) -> Dict[str, Any]:
        account_repository_mock = mocker.Mock(interfaces.AccountRepositoryInterface)
        account_repository_mock.create.return_value = account
        return {
            "account_repository": account_repository_mock,
        }

    return _factory


def test__create_account_use_case__creates_an_account__when_successful(
    mocker: MockFixture,
    fixture_account_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[entities.Account], Dict[str, Any]],
) -> None:
    account = entities.Account(**fixture_account_data)
    dependencies = dependencies_factory(account=account)
    input_dto_validator_mock = mocker.patch(
        "src.interactor.use_cases.create_account.validations.CreateAccountInputDtoValidator"  # noqa
    )
    input_dto_validator_instance = input_dto_validator_mock.return_value
    use_case = use_cases.CreateAccountUseCase(**dependencies)
    request_input = request_models.CreateAccountRequest(
        email=account.email,
        password=account.password,
        user=account.user,
        photo=account.photo,
        role_id=fixture_role_data["role_id"],
        person_id=fixture_person_data["person_id"],
    )
    request_response = response_models.CreateAccountResponse(
        account_id=account.account_id,
        person_id=fixture_person_data["person_id"],
        role_id=fixture_role_data["role_id"],
    )
    response = use_case.execute(request_input)

    dependencies["account_repository"].create.assert_called_once()
    input_dto_validator_mock.assert_called_once_with(asdict(request_input))
    input_dto_validator_instance.validate.assert_called_once_with()
    assert response == request_response


def test__create_account_use_case__raises_an_error__when_there_is_a_none_return_value_from_repository(  # noqa
    mocker: MockFixture,
    fixture_account_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[entities.Account], Dict[str, Any]],
) -> None:
    account = entities.Account(**fixture_account_data)
    dependencies = dependencies_factory(account=account)
    dependencies["account_repository"].create.return_value = None
    use_case = use_cases.CreateAccountUseCase(**dependencies)
    request_input = request_models.CreateAccountRequest(
        email=account.email,
        password=account.password,
        user=account.user,
        photo=account.photo,
        role_id=fixture_role_data["role_id"],
        person_id=fixture_person_data["person_id"],
    )
    with pytest.raises(errors.ItemNotCreatedException) as exc_info:
        use_case.execute(request_input)

    assert str(exc_info.value) == f"Account '{account.email}' was not created"


def test__create_account_use_case__raises_an_error__when_there_is_an_empty_field(
    mocker: MockFixture,
    fixture_account_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[entities.Account], Dict[str, Any]],
) -> None:
    account = entities.Account(**fixture_account_data)
    dependencies = dependencies_factory(account=account)
    use_case = use_cases.CreateAccountUseCase(**dependencies)
    request_input = request_models.CreateAccountRequest(
        email=account.email,
        password=account.password,
        user="",
        photo=account.photo,
        role_id=fixture_role_data["role_id"],
        person_id=fixture_person_data["person_id"],
    )
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(request_input)

    assert str(exc_info.value) == "user: empty values not allowed"
    dependencies["account_repository"].create.assert_not_called()
