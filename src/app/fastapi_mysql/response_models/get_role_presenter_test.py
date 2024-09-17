from typing import Any, Dict

from src.domain import Role
from src.domain.request_models import GetRoleOutputDto

from . import GetRolePresenter


def test_get_role_presenter(fixture_role_data: Dict[str, Any]) -> None:
    role = Role(**fixture_role_data)
    output_dto = GetRoleOutputDto(role)
    presenter = GetRolePresenter()
    response = presenter.present(output_dto)
    assert response == {
        "role_id": fixture_role_data["role_id"],
        "role_name": fixture_role_data["role_name"],
        "description": fixture_role_data["description"],
    }
