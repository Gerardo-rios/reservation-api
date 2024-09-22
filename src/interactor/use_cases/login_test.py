from typing import Any, Callable, Dict, Optional

import pytest
from pytest_mock import MockFixture

from src.domain import entities, interfaces
from src.interactor import errors, request_models, response_models, use_cases


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[[entities.Account], Dict[str, Any]]:
    def _dependencies_factory(account: entities.Account) -> Dict[str, Any]:
        login_repository_mock = mocker.Mock(interfaces.LoginRepositoryInterface)
        login_repository_mock.login.return_value = account
        return {
            "login_repository": login_repository_mock,
        }

    return _dependencies_factory


def test__login_use_case__returns_an_account_id__when_successful(
    mocker: MockFixture,
    fixture_account_data: Dict[str, Any],
    dependencies_factory: Callable[[entities.Account], Dict[str, Any]],
) -> None:
    account = entities.Account(**fixture_account_data)
    dependencies = dependencies_factory(account)
    use_case = use_cases.LoginUseCase(**dependencies)
    request_input = request_models.LoginRequest(
        email=fixture_account_data["email"],
        password=fixture_account_data["password"],
    )
    request_response = response_models.LoginResponse(account=account.account_id)

    response = use_case.execute(request_input)

    dependencies["login_repository"].login.assert_called_once()
    assert response == request_response


def test__login_use_case__returns_none__when_it_fails(
    mocker: MockFixture,
    dependencies_factory: Callable[
        [Optional[response_models.LoginResponse]], Dict[str, Any]
    ],
) -> None:
    dependencies = dependencies_factory(None)
    use_case = use_cases.LoginUseCase(**dependencies)
    input_dto = request_models.LoginRequest(
        email="mail_not_found@gmail.com",
        password="super_secret_password",
    )

    with pytest.raises(errors.AuthenticationError) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == "Invalid email or password provided"
    dependencies["login_repository"].login.assert_called_once()
