from typing import Any, Callable, Dict, Optional

import jwt
import pytest
from pytest_mock import MockFixture

from src.domain import LoginSession
from src.interactor.errors import AuthenticationError
from src.interactor.interfaces import LoginPresenterInterface, LoginRepositoryInterface
from src.interactor.request_models import LoginInputDto, LoginOutputDto
from src.interactor.use_cases import LoginUseCase


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[[LoginSession], Dict[str, Any]]:
    def _dependencies_factory(session: LoginSession) -> Dict[str, Any]:
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
    dependencies_factory: Callable[[LoginSession], Dict[str, Any]],
) -> None:
    session = LoginSession(
        account={
            "account_id": fixture_account_data["account_id"],
            "email": fixture_account_data["email"],
            "user": fixture_account_data["user"],
            "photo": fixture_account_data["photo"],
        },
        person={
            "person_id": fixture_person_data["person_id"],
            "name": fixture_person_data["name"],
            "phone": fixture_person_data["phone"],
            "address": fixture_person_data["address"],
        },
        role={
            "role_id": fixture_role_data["role_id"],
            "role_name": fixture_role_data["role_name"],
        },
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
