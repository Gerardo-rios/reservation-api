from typing import Any, Dict
from src.interactor import CreateAccountOutputDto
from src.domain import Account
from . import CreateAccountPresenter


def test_create_account_presenter(
    fixture_account_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
) -> None:
    account = Account(**fixture_account_data)
    output_dto = CreateAccountOutputDto(
        account, fixture_role_data["role_id"], fixture_person_data["person_id"]
    )
    presenter = CreateAccountPresenter()
    response = presenter.present(output_dto)
    assert response == {
        "account_id": fixture_account_data["account_id"],
        "email": fixture_account_data["email"],
        "user": fixture_account_data["user"],
        "photo": fixture_account_data["photo"],
        "status": fixture_account_data["status"],
        "person_id": fixture_person_data["person_id"],
        "role_id": fixture_role_data["role_id"],
    }
