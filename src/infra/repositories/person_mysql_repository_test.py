import pytest
from unittest.mock import Mock
from pytest_mock import MockerFixture
import uuid
from typing import Dict, Any
from src.infra import PersonDBModel
from src.domain import Person
from src.interactor import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from . import PersonMySQLRepository


@pytest.fixture
def test_setup(mocker: MockerFixture) -> Dict[str, Any]:
    mock_uuid = mocker.patch("uuid.uuid4")
    mock_uuid.return_value = uuid.UUID("fa360eeb-f000-4fca-a737-71b239d88b5e")

    mock_session = Mock()
    mock_db_model = mocker.patch(
        "src.infra.repositories.person_mysql_repository.PersonDBModel"
    )

    test_data = {
        "new_person": {
            "person_id": "fa360eeb-f000-4fca-a737-71b239d88b5e",
            "name": "John Doe",
            "phone": "1234567890",
            "address": "1234 Elm St",
            "city": "Loja",
            "country": "Ecuador",
        },
    }

    mock_db_model.return_value = PersonDBModel(**test_data["new_person"])

    mocker.patch(
        "src.infra.repositories.person_mysql_repository.Session",
        return_value=mock_session,
    )

    repository = PersonMySQLRepository()
    repository._PersonMySQLRepository__session = mock_session

    return {
        "repository": repository,
        "mock_session": mock_session,
        "test_data": test_data,
        "mock_db_model": mock_db_model,
    }


def test_mysql_person_repository_create_person(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    person = repository.create(
        test_data["new_person"]["name"],
        test_data["new_person"]["phone"],
        test_data["new_person"]["address"],
        test_data["new_person"]["city"],
        test_data["new_person"]["country"],
    )

    assert person is not None
    assert person.person_id == test_data["new_person"]["person_id"]
    assert person.name == test_data["new_person"]["name"]
    assert person.phone == test_data["new_person"]["phone"]
    assert person.address == test_data["new_person"]["address"]
    assert person.city == test_data["new_person"]["city"]
    assert person.country == test_data["new_person"]["country"]


def test_mysql_person_repository_create_person_unique_violation(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]

    repository._PersonMySQLRepository__session.add.side_effect = IntegrityError(
        "IntegrityError", "IntegrityError", "IntegrityError"
    )

    with pytest.raises(UniqueViolationError):
        repository.create(
            test_data["new_person"]["name"],
            test_data["new_person"]["phone"],
            test_data["new_person"]["address"],
            test_data["new_person"]["city"],
            test_data["new_person"]["country"],
        )

    repository._PersonMySQLRepository__session.rollback.assert_called_once()
    repository._PersonMySQLRepository__session.add.assert_called_once()
    repository._PersonMySQLRepository__session.commit.assert_not_called()
    repository._PersonMySQLRepository__session.refresh.assert_not_called()


def test_mysql_person_repository_get_person(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]
    person = repository.create(
        test_data["new_person"]["name"],
        test_data["new_person"]["phone"],
        test_data["new_person"]["address"],
        test_data["new_person"]["city"],
        test_data["new_person"]["country"],
    )
    repository._PersonMySQLRepository__session.query.return_value.filter_by.return_value.first.return_value = (  # noqa E501
        person
    )

    person = repository.get(person.person_id)

    assert person is not None
    assert person.person_id == test_data["new_person"]["person_id"]
    assert person.name == test_data["new_person"]["name"]
    assert person.phone == test_data["new_person"]["phone"]
    assert person.address == test_data["new_person"]["address"]
    assert person.city == test_data["new_person"]["city"]
    assert person.country == test_data["new_person"]["country"]
    repository._PersonMySQLRepository__session.query.return_value.filter_by.return_value.first.return_value = test_data[  # noqa E501
        "new_person"
    ]
    repository._PersonMySQLRepository__session.query.assert_called_once()
    repository._PersonMySQLRepository__session.query.return_value.filter_by.assert_called_once()  # noqa E501
    repository._PersonMySQLRepository__session.query.return_value.filter_by.return_value.first.assert_called_once()  # noqa E501


def test_mysql_person_repository_get_person_not_found(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]
    repository._PersonMySQLRepository__session.query.return_value.filter_by.return_value.first.return_value = (  # noqa E501
        None
    )
    person = repository.get(test_data["new_person"]["person_id"])

    assert person is None
    repository._PersonMySQLRepository__session.query.return_value.filter_by.return_value.first.return_value = test_data[  # noqa E501
        "new_person"
    ]
    repository._PersonMySQLRepository__session.query.assert_called_once()
    repository._PersonMySQLRepository__session.query.return_value.filter_by.assert_called_once()  # noqa E501
    repository._PersonMySQLRepository__session.query.return_value.filter_by.return_value.first.assert_called_once()  # noqa E501


def test_mysql_person_repository_update_person(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]
    mock_db_model = test_setup["mock_db_model"]
    person = Person(
        person_id=test_data["new_person"]["person_id"],
        name="Jane Doe",
        phone="0987654321",
        address="4321 Oak St",
        city=test_data["new_person"]["city"],
        country=test_data["new_person"]["country"],
    )
    mock_db_model.return_value = PersonDBModel(**person.to_dict())
    repository._PersonMySQLRepository__session.query.return_value.filter_by.return_value.update.return_value = (  # noqa E50
        1
    )

    updated_person = repository.update(person)

    assert updated_person is not None
    assert updated_person.person_id == test_data["new_person"]["person_id"]
    assert updated_person.name == "Jane Doe"
    assert updated_person.phone == "0987654321"
    assert updated_person.address == "4321 Oak St"
    repository._PersonMySQLRepository__session.query.assert_called_once()
    repository._PersonMySQLRepository__session.query.return_value.filter_by.assert_called_once()  # noqa E501
    repository._PersonMySQLRepository__session.query.return_value.filter_by.return_value.update.assert_called_once()  # noqa E501


def test_mysql_person_repository_update_person_not_found(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    test_data = test_setup["test_data"]
    mock_db_model = test_setup["mock_db_model"]
    person = Person(
        person_id=test_data["new_person"]["person_id"],
        name="Jane Doe",
        phone="0987654321",
        address="4321 Oak St",
        city=test_data["new_person"]["city"],
        country=test_data["new_person"]["country"],
    )
    mock_db_model.return_value = PersonDBModel(**person.to_dict())
    repository._PersonMySQLRepository__session.query.return_value.filter_by.return_value.update.return_value = (  # noqa
        0
    )

    updated_person = repository.update(person)

    assert updated_person is None
    repository._PersonMySQLRepository__session.query.assert_called_once()
    repository._PersonMySQLRepository__session.query.return_value.filter_by.assert_called_once()  # noqa E501
    repository._PersonMySQLRepository__session.query.return_value.filter_by.return_value.update.assert_called_once()  # noqa E501
