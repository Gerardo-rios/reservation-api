import uuid
from typing import Any, Dict
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.exc import IntegrityError

from src.domain import entities
from src.infra import db_models
from src.interactor import errors

from . import AccountMySQLRepository


@pytest.fixture
def test_setup(mocker: MockerFixture) -> Dict[str, Any]:
    mock_uuid = mocker.patch("uuid.uuid4")
    mock_uuid.return_value = uuid.UUID("fa360eeb-f000-4fca-a737-71b239d88b5e")

    mock_session = Mock()
    mock_account_db_model = mocker.patch(
        "src.infra.repositories.account_mysql_repository.db_models.AccountDBModel"
    )
    mock_person_db_model = mocker.patch(
        "src.infra.repositories.account_mysql_repository.db_models.PersonDBModel"
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
        },
        "new_person": {
            "person_id": "test_person_id",
            "name": "Test Person",
            "phone": "1234567890",
            "address": "Test Address",
            "city": "Test City",
            "country": "Test Country",
        },
    }

    mock_account_db_model.return_value = db_models.AccountDBModel(**test_data["new_account"])  # type: ignore  # noqa
    mock_person_db_model.return_value = db_models.PersonDBModel(**test_data["new_person"])  # type: ignore  # noqa

    mocker.patch(
        "src.infra.repositories.account_mysql_repository.db_models.db_base.Session",
        return_value=mock_session,
    )

    repository = AccountMySQLRepository()
    repository._AccountMySQLRepository__session = mock_session

    return {
        "repository": repository,
        "mock_session": mock_session,
        "test_data": test_data,
        "mock_account_db_model": mock_account_db_model,
        "mock_person_db_model": mock_person_db_model,
    }


def test__mysql_account_repository__create_account__succeeds__when_data_is_valid(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    mock_account_instance = test_setup["mock_account_db_model"].return_value
    mock_account_instance.account_id = test_data["new_account"]["account_id"]
    mock_account_instance.email = test_data["new_account"]["email"]
    mock_account_instance.password = test_data["new_account"]["password"]
    mock_account_instance.username = test_data["new_account"]["username"]
    mock_account_instance.photo = test_data["new_account"]["photo"]
    mock_account_instance.status = test_data["new_account"]["status"]

    account = repository.create(
        email=test_data["new_account"]["email"],
        password=test_data["new_account"]["password"],
        user=test_data["new_account"]["username"],
        photo=test_data["new_account"]["photo"],
        status=test_data["new_account"]["status"],
        role_id=test_data["new_account"]["role_id"],
        person_id=test_data["new_account"]["person_id"],
    )

    assert account is not None
    assert account.account_id == test_data["new_account"]["account_id"]
    assert account.email == test_data["new_account"]["email"]
    assert account.password == test_data["new_account"]["password"]
    assert account.user == test_data["new_account"]["username"]
    assert account.photo == test_data["new_account"]["photo"]
    assert account.status == test_data["new_account"]["status"]


def test__mysql_account_repository__create_account__fails__when_account_already_exists(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    repository._AccountMySQLRepository__session.add.side_effect = IntegrityError(
        "IntegrityError", "IntegrityError", "IntegrityError"
    )

    with pytest.raises(errors.UniqueViolationError):
        repository.create(
            email=test_data["new_account"]["email"],
            password=test_data["new_account"]["password"],
            user=test_data["new_account"]["username"],
            photo=test_data["new_account"]["photo"],
            status=test_data["new_account"]["status"],
            role_id=test_data["new_account"]["role_id"],
            person_id=test_data["new_account"]["person_id"],
        )


def test__mysql_account_repository__get_account__returns_account__when_account_exists(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    mock_account_instance = test_setup["mock_account_db_model"].return_value
    mock_account_instance.account_id = test_data["new_account"]["account_id"]
    mock_account_instance.email = test_data["new_account"]["email"]
    mock_account_instance.password = test_data["new_account"]["password"]
    mock_account_instance.username = test_data["new_account"]["username"]
    mock_account_instance.photo = test_data["new_account"]["photo"]
    mock_account_instance.status = test_data["new_account"]["status"]
    mock_account_instance.role_id = test_data["new_account"]["role_id"]
    mock_account_instance.person_id = test_data["new_account"]["person_id"]

    repository._AccountMySQLRepository__session.query.return_value.filter_by.return_value.first.return_value = (  # noqa
        mock_account_instance
    )

    result = repository.get(account_id=test_data["new_account"]["account_id"])

    assert isinstance(result["account"], entities.Account)
    assert result["account"].account_id == test_data["new_account"]["account_id"]
    assert result["account"].email == test_data["new_account"]["email"]
    assert result["account"].password == test_data["new_account"]["password"]
    assert result["account"].user == test_data["new_account"]["username"]
    assert result["account"].photo == test_data["new_account"]["photo"]
    assert result["account"].status == test_data["new_account"]["status"]
    assert result["role_id"] == test_data["new_account"]["role_id"]
    assert result["person_id"] == test_data["new_account"]["person_id"]


def test__mysql_account_repository__get_account__returns_none__when_account_does_not_exist(  # noqa
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    repository._AccountMySQLRepository__session.query.return_value.filter_by.return_value.first.return_value = (  # noqa
        None
    )

    result = repository.get(account_id=test_data["new_account"]["account_id"])

    assert result is None


def test__mysql_account_repository__update_account__succeeds__with_valid_data(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    account = entities.Account(
        account_id=test_data["new_account"]["account_id"],
        email=test_data["new_account"]["email"],
        password="new_Strong_passw0rd!",
        user=test_data["new_account"]["username"],
        photo="new_photo",
        status=test_data["new_account"]["status"],
    )

    mock_account_instance = test_setup["mock_account_db_model"].return_value
    mock_account_instance.account_id = account.account_id
    mock_account_instance.email = account.email
    mock_account_instance.password = account.password
    mock_account_instance.username = account.user
    mock_account_instance.photo = account.photo
    mock_account_instance.status = account.status

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


def test__mysql_account_repository__update_account__raises_error__for_non_existent_account(  # noqa
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]
    mock_account_db_model = test_setup["mock_account_db_model"]
    account = entities.Account(
        account_id=test_data["new_account"]["account_id"],
        email=test_data["new_account"]["email"],
        password="new_Strong_passw0rd!",
        user=test_data["new_account"]["username"],
        photo="new_photo",
        status=test_data["new_account"]["status"],
    )
    mock_account_db_model.return_value = db_models.AccountDBModel(
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
