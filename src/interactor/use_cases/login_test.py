from typing import Any, Callable, Dict, Optional

import jwt
import pytest
from pytest_mock import MockFixture

from src.domain import Account, Person, Role, Session
from src.interactor.dtos import LoginInputDto, LoginOutputDto
from src.interactor.errors import AuthenticationError
from src.interactor.interfaces import LoginPresenterInterface, LoginRepositoryInterface
from src.interactor.use_cases import LoginUseCase


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[[Session], Dict[str, Any]]:
    def _dependencies_factory(session: Session) -> Dict[str, Any]:
        mocker.patch("jwt.encode", return_value="mocked_jwt_token")
        login_repository_mock = mocker.Mock(LoginRepositoryInterface)
        login_repository_mock.login.return_value = session
        presenter_mock = mocker.Mock(LoginPresenterInterface)
        presenter_mock.present.return_value = {
            "login_data": {"token": "mocked_jwt_token", "session": session.to_dict()}
            if session
            else None
        }
        return {
            "login_repository": login_repository_mock,
            "login_presenter": presenter_mock,
        }

    return _dependencies_factory


def test_login_use_case(
    mocker: MockFixture,
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_account_data: Dict[str, Any],
    dependencies_factory: Callable[[Session], Dict[str, Any]],
) -> None:
    session = Session(
        account=Account(**fixture_account_data),
        person=Person(**fixture_person_data),
        role=Role(**fixture_role_data),
    )
    dependencies = dependencies_factory(session)
    use_case = LoginUseCase(**dependencies)
    input_dto = LoginInputDto(
        email=fixture_account_data["email"],
        password=fixture_account_data["password"],
    )
    output_data = LoginOutputDto(token="mocked_jwt_token", session=session)

    response = use_case.execute(input_dto)

    dependencies["login_repository"].login.assert_called_once()
    dependencies["login_presenter"].present.assert_called_once_with(output_data)
    assert response == {
        "login_data": {"token": "mocked_jwt_token", "session": session.to_dict()}
    }
    jwt.encode.assert_called_once()


def test_login_use_case_failure(
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
