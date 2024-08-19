from typing import Any, Dict
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.domain import LoginSession
from src.infra import AccountDBModel, PersonDBModel, RolDBModel

from . import LoginMySQLRepository


@pytest.fixture
def test_setup(
    mocker: MockerFixture,
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> Dict[str, Any]:
    mock_session = Mock()

    test_data = {
        "account": fixture_account_data,
        "person": fixture_person_data,
        "role": fixture_role_data,
    }

    mocker.patch(
        "src.infra.repositories.login_mysql_repository.Session",
        return_value=mock_session,
    )

    repository = LoginMySQLRepository()
    repository._LoginMySQLRepository__session = mock_session

    return {
        "repository": repository,
        "mock_session": mock_session,
        "test_data": test_data,
    }


def test_mysql_login_repository_get_existing_account(
    mocker: MockerFixture, test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]
    test_data = test_setup["test_data"]
    mocker.patch("bcrypt.checkpw", return_value=True)
    db_account = AccountDBModel(
        account_id=test_data["account"]["account_id"],
        email=test_data["account"]["email"],
        password=test_data["account"]["password"],
        username=test_data["account"]["user"],
        photo=test_data["account"]["photo"],
        status=test_data["account"]["status"],
        person_id=test_data["person"]["person_id"],
        role_id=test_data["role"]["role_id"],
    )
    db_person = PersonDBModel(**test_data["person"])
    db_role = RolDBModel(**test_data["role"])

    mock_session.query.return_value.filter_by.return_value.first.side_effect = [
        db_account,
        db_person,
        db_role,
    ]

    result = repository.login(
        email=test_data["account"]["email"], password=test_data["account"]["password"]
    )

    assert isinstance(result, LoginSession)
    assert result.account == {
        "account_id": test_data["account"]["account_id"],
        "email": test_data["account"]["email"],
        "user": test_data["account"]["user"],
        "photo": test_data["account"]["photo"],
    }
    assert result.person == {
        "person_id": test_data["person"]["person_id"],
        "name": test_data["person"]["name"],
        "phone": test_data["person"]["phone"],
        "address": test_data["person"]["address"],
    }
    assert result.role == {
        "role_id": test_data["role"]["role_id"],
        "role_name": test_data["role"]["role_name"],
    }


def test_mysql_login_repository_get_non_existing_role(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]

    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    result = repository.login(
        email="non_existing_email", password="non_existing_password"
    )

    assert result is None
