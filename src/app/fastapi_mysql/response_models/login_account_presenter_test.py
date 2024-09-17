from typing import Any, Dict

from src.domain import Account
from src.domain.request_models import LoginOutputDto

from . import LoginAccountPresenter


def test_get_role_presenter(
    fixture_account_data: Dict[str, Any],
) -> None:
    account = Account(**fixture_account_data)
    output_dto = LoginOutputDto(
        account=account.account_id,
    )
    presenter = LoginAccountPresenter()
    token = "test_token"
    response = presenter.present(output_dto=output_dto, token=token)
    assert response == {
        "token": token,
        "account": account.account_id,
    }
