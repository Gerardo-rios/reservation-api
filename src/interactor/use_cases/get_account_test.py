from typing import Any, Callable, Dict, Optional

import pytest
from pytest_mock import MockFixture

from src.domain import entities, interfaces
from src.interactor import errors, request_models, response_models, use_cases


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[
    [Optional[entities.Account], Optional[str], Optional[str]], Dict[str, Any]
]:
    def _dependencies_factory(
        account: Optional[entities.Account] = None,
        person_id: Optional[str] = None,
        role_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        account_repository_mock = mocker.Mock(interfaces.AccountRepositoryInterface)
        if account is not None:
            account_repository_mock.get.return_value = {
                "account": account,
                "person_id": person_id,
                "role_id": role_id,
            }
        else:
            account_repository_mock.get.return_value = None
        return {
            "account_repository": account_repository_mock,
        }

    return _dependencies_factory


def test__get_account_use_case__returns_an_account__when_successfully(
    mocker: MockFixture,
    fixture_role_data: Dict[str, Any],
    fixture_account_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[
        [Optional[entities.Account], Optional[str], Optional[str]], Dict[str, Any]
    ],
) -> None:
    account = entities.Account(**fixture_account_data)
    person_id = fixture_person_data["person_id"]
    role_id = fixture_role_data["role_id"]
    dependencies = dependencies_factory(account, person_id, role_id)
    use_case = use_cases.GetAccountUseCase(**dependencies)
    request_input = request_models.GetAccountByIdRequest(account_id=account.account_id)
    request_response = response_models.GetAccountResponse(
        account=account, person_id=person_id, role_id=role_id
    )
    response = use_case.execute(request_input)

    dependencies["account_repository"].get.assert_called_once()
    assert response == request_response


def test__get_account__when_it_is_not_found(
    mocker: MockFixture,
    dependencies_factory: Callable[
        [Optional[entities.Account], Optional[str], Optional[str]], Dict[str, Any]
    ],
) -> None:
    dependencies = dependencies_factory(None, None, None)
    use_case = use_cases.GetAccountUseCase(**dependencies)
    input_dto = request_models.GetAccountByIdRequest(
        account_id="no_existing_account_id"
    )

    with pytest.raises(errors.ItemNotFoundException) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == "Account 'no_existing_account_id' was not found"
    dependencies["account_repository"].get.assert_called_once()
