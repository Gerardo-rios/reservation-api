import uuid
from typing import Any, Dict
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.exc import IntegrityError

from src.domain import Person
from src.infra import PersonDBModel
from src.interactor import errors

from .person_mysql_repository import PersonMySQLRepository


@pytest.fixture
def test_setup(mocker: MockerFixture) -> Dict[str, Any]:
    mock_uuid = mocker.patch("uuid.uuid4")
    mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")
    mock_session = Mock()

    test_data = {
        "persons": [
            {
                "person_id": "12345678-1234-5678-1234-567812345678",
                "name": "John Doe",
                "phone": "123456789",
                "address": "123 Main St",
                "city": "Loja",
                "country": "Ecuador",
            }
        ]
    }

    mocker.patch(
        "src.infra.repositories.person_mysql_repository.db_models.db_base.Session",
        return_value=mock_session,
    )

    repository = PersonMySQLRepository()
    repository._PersonMySQLRepository__session = mock_session

    return {
        "repository": repository,
        "mock_session": mock_session,
        "test_data": test_data,
    }


def test__get_person_by_phone__when_the_person_exists_in_database(
    test_setup: Dict[str, Any],
) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]
    test_data = test_setup["test_data"]
    person_data = test_data["persons"][0]

    db_person = PersonDBModel(**person_data)
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        db_person
    )

    result = repository.get_by_phone(phone=person_data["phone"])

    assert isinstance(result, Person)
    assert result.person_id == person_data["person_id"]
    assert result.name == person_data["name"]
    assert result.phone == person_data["phone"]
    assert result.address == person_data["address"]
    assert result.city == person_data["city"]
    assert result.country == person_data["country"]


def test__get_person_by_phone__when_the_person_does_not_exist_in_database(
    test_setup: Dict[str, Any],
) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]

    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    result = repository.get_by_phone(phone="non_existing_phone_number")

    assert result is None


def test__create_person__when_the_person_is_created_successfully(
    test_setup: Dict[str, Any],
) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]
    test_data = test_setup["test_data"]
    person_data = test_data["persons"][0]

    result = repository.create(
        name=person_data["name"],
        phone=person_data["phone"],
        address=person_data["address"],
        city=person_data["city"],
        country=person_data["country"],
    )

    assert result == person_data["person_id"]
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test__create_person__fails__when_a_person_with_the_same_phone_number_already_exists(
    test_setup: Dict[str, Any],
) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]
    test_data = test_setup["test_data"]
    person_data = test_data["persons"][0]

    mock_session.add.side_effect = IntegrityError(
        "IntegrityError", "IntegrityError", "IntegrityError"
    )

    with pytest.raises(errors.UniqueViolationError) as exc_info:
        repository.create(
            name=person_data["name"],
            phone=person_data["phone"],
            address=person_data["address"],
            city=person_data["city"],
            country=person_data["country"],
        )

    assert str(exc_info.value) == "Phone number already exists"
    mock_session.rollback.assert_called_once()
    mock_session.add.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


def test__get_person_by_id__when_the_person_exists_in_database(
    test_setup: Dict[str, Any],
) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]
    test_data = test_setup["test_data"]
    person_data = test_data["persons"][0]

    db_person = PersonDBModel(**person_data)
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        db_person
    )

    result = repository.get_by_id(person_id=person_data["person_id"])

    assert isinstance(result, Person)
    assert result.person_id == person_data["person_id"]
    assert result.name == person_data["name"]
    assert result.phone == person_data["phone"]
    assert result.address == person_data["address"]
    assert result.city == person_data["city"]
    assert result.country == person_data["country"]


def test__get_person_by_id__when_the_person_does_not_exist_in_database(
    test_setup: Dict[str, Any],
) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]

    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    result = repository.get_by_id(person_id="non_existing_person_id")

    assert result is None
