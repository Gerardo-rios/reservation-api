from typing import Any, Dict

from src.domain import LoginSession
from src.interactor.dtos import LoginOutputDto

from . import LoginAccountPresenter


def test_get_role_presenter(
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    fixture_account_data: Dict[str, Any],
) -> None:
    session = LoginSession(
        account={
            "account_id": fixture_account_data["account_id"],
            "email": fixture_account_data["email"],
            "user": fixture_account_data["user"],
            "photo": fixture_account_data["photo"],
        },
        person={
            "person_id": fixture_person_data["person_id"],
            "name": fixture_person_data["name"],
            "phone": fixture_person_data["phone"],
            "address": fixture_person_data["address"],
        },
        role={
            "role_id": fixture_role_data["role_id"],
            "role_name": fixture_role_data["role_name"],
        },
    )
    output_dto = LoginOutputDto(
        token="test_token",
        session=session,
    )
    presenter = LoginAccountPresenter()
    response = presenter.present(output_dto)
    assert response == {
        "token": "test_token",
        "session": session.to_dict(),
    }
