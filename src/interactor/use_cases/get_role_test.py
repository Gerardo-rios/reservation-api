from typing import Any, Callable, Dict, Optional

import pytest
from pytest_mock import MockFixture

from src.domain import Role
from src.interactor.errors import ItemNotFoundException
from src.interactor.interfaces import GetRolePresenterInterface, RoleRepositoryInterface
from src.interactor.request_models import GetRoleInputDto, GetRoleOutputDto
from src.interactor.use_cases import GetRoleUseCase


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[[Role], Dict[str, Any]]:
    def _dependencies_factory(role: Optional[Role] = None) -> Dict[str, Any]:
        role_repository_mock = mocker.Mock(RoleRepositoryInterface)
        role_repository_mock.get.return_value = role
        presenter_mock = mocker.Mock(GetRolePresenterInterface)
        presenter_mock.present.return_value = {"role": role.to_dict() if role else None}
        return {
            "role_repository": role_repository_mock,
            "role_presenter": presenter_mock,
        }

    return _dependencies_factory


def test_get_role(
    mocker: MockFixture,
    fixture_role_data: Dict[str, Any],
    dependencies_factory: Callable[[Optional[Role]], Dict[str, Any]],
) -> None:
    role = Role(**fixture_role_data)
    dependencies = dependencies_factory(role)
    use_case = GetRoleUseCase(**dependencies)
    input_dto = GetRoleInputDto(role_name=role.role_name)
    output_dto = GetRoleOutputDto(role)
    response = use_case.execute(input_dto)

    dependencies["role_repository"].get.assert_called_once()
    dependencies["role_presenter"].present.assert_called_once_with(output_dto)
    assert response == {"role": role.to_dict()}


def test_get_role__when_it_is_not_found(
    mocker: MockFixture,
    dependencies_factory: Callable[[Optional[Role]], Dict[str, Any]],
    fixture_role_data: Dict[str, Any],
) -> None:
    dependencies = dependencies_factory(None)
    use_case = GetRoleUseCase(**dependencies)
    input_dto = GetRoleInputDto(role_name="invalid_role_name")

    with pytest.raises(ItemNotFoundException) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == "Role 'invalid_role_name' was not found"
    dependencies["role_repository"].get.assert_called_once()
    dependencies["role_presenter"].present.assert_not_called()
