from typing import Any, Dict
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.domain import Role
from src.infra import RolDBModel

from . import RolMySQLRepository


@pytest.fixture
def test_setup(mocker: MockerFixture) -> Dict[str, Any]:
    mock_session = Mock()

    test_data = {
        "default_roles": [
            {
                "role_id": "12345678-1234-5678-1234-567812345678",
                "role_name": "admin",
                "description": "Administrator with business permissions",
            },
            {
                "role_id": "87654321-4321-8765-4321-876543210987",
                "role_name": "user",
                "description": "User with user usage permissions",
            },
        ]
    }

    mocker.patch(
        "src.infra.repositories.rol_mysql_repository.Session", return_value=mock_session
    )

    repository = RolMySQLRepository()
    repository._RolMySQLRepository__session = mock_session

    return {
        "repository": repository,
        "mock_session": mock_session,
        "test_data": test_data,
    }


def test_mysql_rol_repository_get_existing_role(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]
    test_data = test_setup["test_data"]
    role_data = test_data["default_roles"][0]

    db_role = RolDBModel(**role_data)
    mock_session.query.return_value.filter_by.return_value.first.return_value = db_role

    result = repository.get(role_name=role_data["role_name"])

    assert isinstance(result, Role)
    assert result.role_id == role_data["role_id"]
    assert result.role_name == role_data["role_name"]
    assert result.description == role_data["description"]


def test_mysql_rol_repository_get_non_existing_role(test_setup: Dict[str, Any]) -> None:
    repository = test_setup["repository"]
    mock_session = test_setup["mock_session"]

    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    result = repository.get(role_name="non_existing")

    assert result is None
