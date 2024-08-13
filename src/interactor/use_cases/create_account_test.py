import pytest
from typing import Any, Dict, Callable
from pytest_mock import MockFixture
from src.domain import Account
from src.interactor import (
    CreateAccountInputDto,
    CreateAccountOutputDto,
    CreateAccountPresenterInterface,
    AccountRepositoryInterface,
    ItemNotCreatedException,
    CreateAccountUseCase,
)


@pytest.fixture
def dependencies_factory(mocker: MockFixture) -> Callable[[Account], Dict[str, Any]]:
    def _factory(account: Account) -> Dict[str, Any]:
        account_repository_mock = mocker.Mock(AccountRepositoryInterface)
        account_repository_mock.create.return_value = account
        presenter_mock = mocker.Mock(CreateAccountPresenterInterface)
        presenter_mock.present.return_value = {"account": account.to_dict()}
        return {
            "account_repository": account_repository_mock,
            "presenter": presenter_mock,
        }

    return _factory


def test_create_account(
    mocker: MockFixture,
    fixture_account_data: Dict[str, Any],
    fixture_rol_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[Account], Dict[str, Any]],
) -> None:
    account = Account(**fixture_account_data)
    dependencies = dependencies_factory(account)
    input_dto_validator_mock = mocker.patch(
        "src.interactor.use_cases.create_account.CreateAccountInputDtoValidator"
    )
    input_dto_validator_instance = input_dto_validator_mock.return_value
    use_case = CreateAccountUseCase(**dependencies)
    input_dto = CreateAccountInputDto(
        email=account.email,
        password=account.password,
        user=account.user,
        photo=account.photo,
        rol_id=fixture_rol_data["rol_id"],
        person_id=fixture_person_data["person_id"],
    )
    output_dto = CreateAccountOutputDto(
        account, fixture_rol_data["rol_id"], fixture_person_data["person_id"]
    )
    response = use_case.execute(input_dto)

    dependencies["account_repository"].create.assert_called_once()
    input_dto_validator_mock.assert_called_once_with(input_dto.to_dict())
    input_dto_validator_instance.validate.assert_called_once_with()
    dependencies["presenter"].present.assert_called_once_with(output_dto)
    assert response == {"account": account.to_dict()}


def test_create_account_with_a_none_return_value_from_repository(
    mocker: MockFixture,
    fixture_account_data: Dict[str, Any],
    fixture_rol_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[Account], Dict[str, Any]],
) -> None:
    account = Account(**fixture_account_data)
    dependencies = dependencies_factory(account)
    dependencies["account_repository"].create.return_value = None
    use_case = CreateAccountUseCase(**dependencies)
    input_dto = CreateAccountInputDto(
        email=account.email,
        password=account.password,
        user=account.user,
        photo=account.photo,
        rol_id=str(fixture_rol_data["rol_id"]),
        person_id=str(fixture_person_data["person_id"]),
    )
    with pytest.raises(ItemNotCreatedException) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == f"Account '{account.email}' was not created"


def test_create_account_with_an_empty_field(
    mocker: MockFixture,
    fixture_account_data: Dict[str, Any],
    fixture_rol_data: Dict[str, Any],
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[Account], Dict[str, Any]],
) -> None:
    account = Account(**fixture_account_data)
    dependencies = dependencies_factory(account)
    use_case = CreateAccountUseCase(**dependencies)
    input_dto = CreateAccountInputDto(
        email=account.email,
        password=account.password,
        user="",
        photo=account.photo,
        rol_id=str(fixture_rol_data["rol_id"]),
        person_id=str(fixture_person_data["person_id"]),
    )
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == "user: empty values not allowed"
    dependencies["account_repository"].create.assert_not_called()
    dependencies["presenter"].present.assert_not_called()
