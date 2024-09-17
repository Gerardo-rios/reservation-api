from typing import Any, Dict

from src.domain import Account, Person
from src.domain.request_models import CreateAccountOutputDto

from . import CreateAccountPresenter


def test_create_account_presenter(
    fixture_account_data: Dict[str, Any],
    fixture_role_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
) -> None:
    account = Account(**fixture_account_data)
    person = Person(**fixture_person_data)
    output_dto = CreateAccountOutputDto(
        account=account, person=person, role_id=fixture_role_data["role_id"]
    )
    presenter = CreateAccountPresenter()
    response = presenter.present(output_dto)
    assert response == {
        "account_id": fixture_account_data["account_id"],
        "email": fixture_account_data["email"],
        "person_id": fixture_person_data["person_id"],
        "person_name": fixture_person_data["name"],
        "role_id": str(fixture_role_data["role_id"]),
        "message": "Account created successfully",
    }
