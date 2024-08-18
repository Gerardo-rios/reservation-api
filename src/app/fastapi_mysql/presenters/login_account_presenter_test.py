from typing import Any, Dict

from src.interactor.dtos import LoginOutputDto

from . import LoginAccountPresenter


def test_get_role_presenter(
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_account_data: Dict[str, Any],
) -> None:
    output_dto = LoginOutputDto(
        token="test_token",
        email=fixture_account_data["email"],
        photo=fixture_account_data["photo"],
        user=fixture_account_data["user"],
        name=fixture_person_data["name"],
        phone=fixture_person_data["phone"],
        address=fixture_person_data["address"],
        role=fixture_role_data["role_name"],
    )
    presenter = LoginAccountPresenter()
    response = presenter.present(output_dto)
    assert response == {
        "token": "test_token",
        "email": fixture_account_data["email"],
        "photo": fixture_account_data["photo"],
        "user": fixture_account_data["user"],
        "name": fixture_person_data["name"],
        "phone": fixture_person_data["phone"],
        "address": fixture_person_data["address"],
        "role": fixture_role_data["role_name"],
    }
