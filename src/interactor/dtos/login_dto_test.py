from typing import Any, Dict

from src.domain import Account, Person, Role, Session

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


def test_create_login_output_dto(
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
) -> None:
    session = Session(
        account=Account(**fixture_account_data),
        person=Person(**fixture_person_data),
        role=Role(**fixture_role_data),
    )
    output_dto = LoginOutputDto(token="test_token", session=session)

    assert output_dto.token == "test_token"
    assert output_dto.session == session
