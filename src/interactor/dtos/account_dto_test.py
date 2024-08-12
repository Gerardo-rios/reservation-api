from typing import Any, Dict
from . import CreateAccountInputDto


def test_create_account_input_dto(
    fixture_account_data: Dict[str, Any],
    fixture_rol_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
) -> None:
    del fixture_account_data["account_id"]
    del fixture_account_data["status"]
    input_dto = CreateAccountInputDto(
        **fixture_account_data,
        rol_id=fixture_rol_data["rol_id"],
        person_id=fixture_person_data["person_id"]
    )

    assert input_dto.to_dict() == {
        "email": fixture_account_data["email"],
        "password": fixture_account_data["password"],
        "user": fixture_account_data["user"],
        "photo": fixture_account_data["photo"],
        "rol_id": fixture_rol_data["rol_id"],
        "person_id": fixture_person_data["person_id"],
    }