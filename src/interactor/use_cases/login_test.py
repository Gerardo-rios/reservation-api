from typing import Any, Callable, Dict, Optional

import pytest
from pytest_mock import MockFixture

from src.domain import Account
from src.interactor.errors import AuthenticationError
from src.interactor.interfaces import LoginPresenterInterface, LoginRepositoryInterface
from src.interactor.request_models import LoginInputDto, LoginOutputDto
from src.interactor.use_cases import LoginUseCase


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[[Account], Dict[str, Any]]:
    def _dependencies_factory(account: Account) -> Dict[str, Any]:
        login_repository_mock = mocker.Mock(LoginRepositoryInterface)
        login_repository_mock.login.return_value = account
        presenter_mock = mocker.Mock(LoginPresenterInterface)
        presenter_mock.present.return_value = {
            "account": account.account_id if account else None
        }
        return {
            "login_repository": login_repository_mock,
            "login_presenter": presenter_mock,
        }

    return _dependencies_factory


def test__login_use_case__returns_an_account_id__when_successful(
    mocker: MockFixture,
    fixture_account_data: Dict[str, Any],
    dependencies_factory: Callable[[Account], Dict[str, Any]],
) -> None:
    account = Account(**fixture_account_data)
    dependencies = dependencies_factory(account)
    use_case = LoginUseCase(**dependencies)
    input_dto = LoginInputDto(
        email=fixture_account_data["email"],
        password=fixture_account_data["password"],
    )
    output_data = LoginOutputDto(account=account.account_id)

    response = use_case.execute(input_dto)

    dependencies["login_repository"].login.assert_called_once()
    dependencies["login_presenter"].present.assert_called_once_with(
        output_dto=output_data, token=None
    )
    assert response == {"account": account.account_id}


def test__login_use_case__returns_none__when_it_fails(
    mocker: MockFixture,
    dependencies_factory: Callable[[Optional[LoginOutputDto]], Dict[str, Any]],
) -> None:
    dependencies = dependencies_factory(None)
    use_case = LoginUseCase(**dependencies)
    input_dto = LoginInputDto(
        email="mail_not_found@gmail.com",
        password="super_secret_password",
    )

    with pytest.raises(AuthenticationError) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == "Invalid email or password provided"
    dependencies["login_repository"].login.assert_called_once()
    dependencies["login_presenter"].present.assert_not_called()
