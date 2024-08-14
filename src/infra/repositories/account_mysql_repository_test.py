import pytest
from unittest.mock import Mock
from pytest_mock import MockerFixture
import uuid
from typing import Dict, Any
from src.infra import AccountDBModel
from src.domain import Account
from src.interactor import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from . import AccountMySQLRepository


@pytest.fixture
def test_setup(mocker: MockerFixture) -> Dict[str, Any]:
    mock_uuid = mocker.patch("uuid.uuid4")
    mock_uuid.return_value = uuid.UUID("fa360eeb-f000-4fca-a737-71b239d88b5e")

    mock_session = Mock()
    mock_db_model = mocker.patch(
        "src.infra.repositories.account_mysql_repository.AccountDBModel"
    )

    test_data = {
        "new_account": {
            "account_id": "fa360eeb-f000-4fca-a737-71b239d88b5e",
            "email": "test_mail@gmail.com",
            "password": "T3st_strong_password!",
            "username": "test_user",
            "photo": "test_photo",
            "status": True,
            "role_id": "test_rol_id",
            "person_id": "test_person_id",
        }
    }

    mock_db_model.return_value = AccountDBModel(**test_data["new_account"])

    mocker.patch(
        "src.infra.repositories.account_mysql_repository.Session",
        return_value=mock_session,
    )

    repository = AccountMySQLRepository()
    repository._AccountMySQLRepository__session = mock_session

    return {
        "repository": repository,
        "mock_session": mock_session,
        "test_data": test_data,
        "mock_db_model": mock_db_model,
    }


def test_mysql_account_repository_create_account(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    account = repository.create(
        test_data["new_account"]["email"],
        test_data["new_account"]["password"],
        test_data["new_account"]["username"],
        test_data["new_account"]["photo"],
        test_data["new_account"]["status"],
        test_data["new_account"]["role_id"],
        test_data["new_account"]["person_id"],
    )

    assert account is not None
    assert account.account_id == test_data["new_account"]["account_id"]
    assert account.email == test_data["new_account"]["email"]
    assert account.password == test_data["new_account"]["password"]
    assert account.user == test_data["new_account"]["username"]
    assert account.photo == test_data["new_account"]["photo"]
    assert account.status == test_data["new_account"]["status"]


def test_mysql_account_repository_create_account_unique_violation(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    repository._AccountMySQLRepository__session.add.side_effect = IntegrityError(
        "IntegrityError", "IntegrityError", "IntegrityError"
    )

    with pytest.raises(UniqueViolationError):
        repository.create(
            test_data["new_account"]["email"],
            test_data["new_account"]["password"],
            test_data["new_account"]["username"],
            test_data["new_account"]["photo"],
            test_data["new_account"]["status"],
            test_data["new_account"]["role_id"],
            test_data["new_account"]["person_id"],
        )


def test_mysql_account_repository_get_existing_account(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    db_account = AccountDBModel(**test_data["new_account"])
    repository._AccountMySQLRepository__session.query.return_value.filter_by.return_value.first.return_value = (  # noqa
        db_account
    )

    result = repository.get(account_id=test_data["new_account"]["account_id"])

    assert isinstance(result, Account)
    assert result.account_id == test_data["new_account"]["account_id"]
    assert result.email == test_data["new_account"]["email"]
    assert result.password == test_data["new_account"]["password"]
    assert result.user == test_data["new_account"]["username"]
    assert result.photo == test_data["new_account"]["photo"]
    assert result.status == test_data["new_account"]["status"]


def test_mysql_account_repository_get_non_existing_account(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    repository._AccountMySQLRepository__session.query.return_value.filter_by.return_value.first.return_value = (  # noqa
        None
    )

    result = repository.get(account_id=test_data["new_account"]["account_id"])

    assert result is None


def test_mysql_account_repository_update_account(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]
    mock_db_model = test_setup["mock_db_model"]
    account = Account(
        account_id=test_data["new_account"]["account_id"],
        email=test_data["new_account"]["email"],
        password="new_Strong_passw0rd!",
        user=test_data["new_account"]["username"],
        photo="new_photo",
        status=test_data["new_account"]["status"],
    )
    mock_db_model.return_value = AccountDBModel(
        account_id=account.account_id,
        email=account.email,
        password=account.password,
        username=account.user,
        photo=account.photo,
        status=account.status,
        role_id=test_data["new_account"]["role_id"],
        person_id=test_data["new_account"]["person_id"],
    )
    repository._AccountMySQLRepository__session.query.return_value.filter_by.return_value.update.return_value = (  # noqa
        1
    )

    result = repository.update(account)

    assert result is not None
    assert result.account_id == account.account_id
    assert result.email == account.email
    assert result.password == account.password
    assert result.user == account.user
    assert result.photo == account.photo
    assert result.status == account.status
    repository._AccountMySQLRepository__session.query.assert_called_once()
    repository._AccountMySQLRepository__session.query.return_value.filter_by.assert_called_once()  # noqa
    repository._AccountMySQLRepository__session.query.return_value.filter_by.return_value.update.assert_called_once()  # noqa


def test_mysql_account_repository_update_non_existing_account(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]
    mock_db_model = test_setup["mock_db_model"]
    account = Account(
        account_id=test_data["new_account"]["account_id"],
        email=test_data["new_account"]["email"],
        password="new_Strong_passw0rd!",
        user=test_data["new_account"]["username"],
        photo="new_photo",
        status=test_data["new_account"]["status"],
    )
    mock_db_model.return_value = AccountDBModel(
        account_id=account.account_id,
        email=account.email,
        password=account.password,
        username=account.user,
        photo=account.photo,
        status=account.status,
        role_id=test_data["new_account"]["role_id"],
        person_id=test_data["new_account"]["person_id"],
    )
    repository._AccountMySQLRepository__session.query.return_value.filter_by.return_value.update.return_value = (  # noqa
        0
    )

    result = repository.update(account)

    assert result is None
    repository._AccountMySQLRepository__session.query.assert_called_once()
    repository._AccountMySQLRepository__session.query.return_value.filter_by.assert_called_once()  # noqa
    repository._AccountMySQLRepository__session.query.return_value.filter_by.return_value.update.assert_called_once()  # noqa
