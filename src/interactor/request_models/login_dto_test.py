from typing import Any, Dict

from . import LoginInputDto, LoginOutputDto


def test_create_login_input_dto(
    fixture_account_data: Dict[str, Any],
) -> None:
    input_dto = LoginInputDto(
        email=fixture_account_data["email"],
        password=fixture_account_data["password"],
    )

    assert input_dto.to_dict() == {
        "email": fixture_account_data["email"],
        "password": fixture_account_data["password"],
    }


def test_create_login_output_dto(fixture_account_data: Dict[str, Any]) -> None:
    output_dto = LoginOutputDto(account=fixture_account_data["account_id"])

    assert output_dto.account == fixture_account_data["account_id"]
