import pytest
from unittest.mock import Mock
from pytest_mock import MockerFixture
import uuid
from typing import Dict, Any
from src.infra import RolDBModel
from src.domain import Rol
from src.interactor import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from . import RolMySQLRepository


@pytest.fixture
def test_setup(mocker: MockerFixture) -> Dict[str, Any]:
    mock_uuid = mocker.patch("uuid.uuid4")
    mock_uuid.side_effect = [
        uuid.UUID("12345678-1234-5678-1234-567812345678"),
        uuid.UUID("87654321-4321-8765-4321-876543210987"),
    ]

    mock_session = Mock()
    mock_db_model = mocker.patch(
        "src.infra.repositories.rol_mysql_repository.RolDBModel"
    )

    test_data = {
        "default_roles": [
            {
                "rol_id": "12345678-1234-5678-1234-567812345678",
                "role_name": "admin",
                "description": "Administrator with business permissions",
            },
            {
                "rol_id": "87654321-4321-8765-4321-876543210987",
                "role_name": "user",
                "description": "User with user usage permissions",
            },
        ],
        "new_role": {
            "rol_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "role_name": "manager",
            "description": "Manager role",
        },
    }

    mock_db_model.side_effect = [
        RolDBModel(**test_data["default_roles"][0]),  # type: ignore
        RolDBModel(**test_data["default_roles"][1]),  # type: ignore
    ]

    mocker.patch(
        "src.infra.repositories.rol_mysql_repository.Session", return_value=mock_session
    )

    repository = RolMySQLRepository()
    repository._RolMySQLRepository__session = mock_session

    return {
        "repository": repository,
        "mock_session": mock_session,
        "mock_db_model": mock_db_model,
        "mock_uuid": mock_uuid,
        "test_data": test_data,
    }


def test_mysql_rol_repository_create_default_roles(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]

    result = repository.create()

    mock_session.add_all.assert_called_once()
    mock_session.commit.assert_called_once()

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(role, Rol) for role in result)
    assert [role.rol_name for role in result] == ["admin", "user"]
    assert [role.description for role in result] == [
        "Administrator with business permissions",
        "User with user usage permissions",
    ]


def test_mysql_rol_repository_repository_create_new_role(
    test_setup: Dict[str, Any]
) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]
    mock_db_model = test_setup["mock_db_model"]
    test_data = test_setup["test_data"]
    new_role = test_data["new_role"]

    mock_db_model.side_effect = None
    mock_db_model.return_value = RolDBModel(**new_role)

    result = repository.create(
        role_name=new_role["role_name"], description=new_role["description"]
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert isinstance(result, Rol)
    assert result.rol_name == new_role["role_name"]
    assert result.description == new_role["description"]


def test_mysql_rol_repository_create_existing_role(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]

    mock_session.add.side_effect = IntegrityError(None, None, None)

    with pytest.raises(UniqueViolationError, match="Role name already exists"):
        repository.create(role_name="admin", description="Test")

    mock_session.rollback.assert_called_once()


def test_mysql_rol_repository_get_existing_role(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]
    test_data = test_setup["test_data"]
    role_data = test_data["default_roles"][0]

    db_role = RolDBModel(**role_data)
    mock_session.query.return_value.filter_by.return_value.first.return_value = db_role

    result = repository.get(role_name=role_data["role_name"])

    assert isinstance(result, Rol)
    assert result.rol_id == role_data["rol_id"]
    assert result.rol_name == role_data["role_name"]
    assert result.description == role_data["description"]


def test_mysql_rol_repository_get_non_existing_role(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]

    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    result = repository.get(role_name="non_existing")

    assert result is None
