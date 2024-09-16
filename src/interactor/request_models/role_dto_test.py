from typing import Any, Dict

from . import GetRoleInputDto


def test_get_role_input_dto(fixture_role_data: Dict[str, Any]) -> None:
    input_dto = GetRoleInputDto(fixture_role_data["role_name"])

    assert input_dto.to_dict() == {"role_name": fixture_role_data["role_name"]}
