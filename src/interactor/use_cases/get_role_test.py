from typing import Any, Callable, Dict, Optional

import pytest
from pytest_mock import MockFixture

from src.domain import entities, interfaces
from src.interactor import errors, request_models, response_models, use_cases


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[[entities.Role], Dict[str, Any]]:
    def _dependencies_factory(role: Optional[entities.Role] = None) -> Dict[str, Any]:
        role_repository_mock = mocker.Mock(interfaces.RoleRepositoryInterface)
        role_repository_mock.get.return_value = role
        return {
            "role_repository": role_repository_mock,
        }

    return _dependencies_factory


def test__get_role_use_case__returns_a_role__when_successfully(
    mocker: MockFixture,
    fixture_role_data: Dict[str, Any],
    dependencies_factory: Callable[[Optional[entities.Role]], Dict[str, Any]],
) -> None:
    role = entities.Role(**fixture_role_data)
    dependencies = dependencies_factory(role)
    use_case = use_cases.GetRoleUseCase(**dependencies)
    request_input = request_models.GetRoleRequest(role_name=role.role_name)
    request_response = response_models.GetRoleResponse(
        role_id=role.role_id, role_name=role.role_name, description=role.description
    )
    response = use_case.execute(request_input)

    dependencies["role_repository"].get.assert_called_once()
    assert response == request_response


def test_get_role__when_it_is_not_found(
    mocker: MockFixture,
    dependencies_factory: Callable[[Optional[entities.Role]], Dict[str, Any]],
    fixture_role_data: Dict[str, Any],
) -> None:
    dependencies = dependencies_factory(None)
    use_case = use_cases.GetRoleUseCase(**dependencies)
    input_dto = request_models.GetRoleRequest(role_name="invalid_role_name")

    with pytest.raises(errors.ItemNotFoundException) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == "Role 'invalid_role_name' was not found"
    dependencies["role_repository"].get.assert_called_once()
