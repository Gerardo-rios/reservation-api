from typing import Any, Dict, Callable
import pytest
from pytest_mock import MockFixture
from src.domain import Person
from src.interactor import (
    CreatePersonUseCase,
    CreatePersonInputDto,
    CreatePersonOutputDto,
    CreatePersonPresenterInterface,
    PersonRepositoryInterface,
    ItemNotCreatedException,
)


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[[Person], Dict[str, Any]]:
    def _dependencies_factory(person: Person) -> Dict[str, Any]:
        person_repository_mock = mocker.Mock(PersonRepositoryInterface)
        person_repository_mock.create.return_value = person
        presenter_mock = mocker.Mock(CreatePersonPresenterInterface)
        presenter_mock.present.return_value = {"person": person.to_dict()}
        return {
            "person_repository": person_repository_mock,
            "presenter": presenter_mock,
        }

    return _dependencies_factory


def test_create_person(
    mocker: MockFixture,
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[Person], Dict[str, Any]],
) -> None:
    person = Person(**fixture_person_data)
    dependencies = dependencies_factory(person)
    input_dto_validator_mock = mocker.patch(
        "src.interactor.use_cases.create_person.CreatePersonInputDtoValidator"
    )
    input_dto_validator_instance = input_dto_validator_mock.return_value
    use_case = CreatePersonUseCase(**dependencies)
    input_dto = CreatePersonInputDto(
        name=person.name,
        phone=person.phone,
        address=person.address,
        city=person.city,
        country=person.country,
    )
    output_dto = CreatePersonOutputDto(person)
    response = use_case.execute(input_dto)

    dependencies["person_repository"].create.assert_called_once()
    input_dto_validator_mock.assert_called_once_with(input_dto.to_dict())
    input_dto_validator_instance.validate.assert_called_once_with()
    dependencies["presenter"].present.assert_called_once_with(output_dto)
    assert response == {"person": person.to_dict()}


def test_create_person_with_a_none_return_value_from_repository(
    mocker: MockFixture,
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[Person], Dict[str, Any]],
) -> None:
    person = Person(**fixture_person_data)
    dependencies = dependencies_factory(person)
    dependencies["person_repository"].create.return_value = None
    use_case = CreatePersonUseCase(**dependencies)
    input_dto = CreatePersonInputDto(
        name=person.name,
        phone=person.phone,
        address=person.address,
        city=person.city,
        country=person.country,
    )
    with pytest.raises(ItemNotCreatedException) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == f"Person '{person.name}' was not created"


def test_create_person_with_an_empty_field(
    mocker: MockFixture,
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[Person], Dict[str, Any]],
) -> None:
    person = Person(**fixture_person_data)
    dependencies = dependencies_factory(person)
    use_case = CreatePersonUseCase(**dependencies)
    input_dto = CreatePersonInputDto(
        name=person.name,
        phone=person.phone,
        address=person.address,
        city=person.city,
        country="",
    )
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == "country: empty values not allowed"
    dependencies["person_repository"].create.assert_not_called()
    dependencies["presenter"].present.assert_not_called()
