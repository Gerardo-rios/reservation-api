from dataclasses import asdict
from typing import Any, Callable, Dict

import pytest
from pytest_mock import MockFixture

from src.domain import entities, interfaces
from src.interactor import errors, request_models, response_models, use_cases


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[[entities.Person], Dict[str, Any]]:
    def _factory(
        person: entities.Person,
    ) -> Dict[str, Any]:
        person_repository_mock = mocker.Mock(interfaces.PersonRepositoryInterface)
        person_repository_mock.create.return_value = person.person_id
        return {
            "person_repository": person_repository_mock,
        }

    return _factory


def test__create_person_use_case__creates_a_person__when_successful(
    mocker: MockFixture,
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[entities.Person], Dict[str, Any]],
) -> None:
    person = entities.Person(**fixture_person_data)
    dependencies = dependencies_factory(person)
    input_dto_validator_mock = mocker.patch(
        "src.interactor.use_cases.create_person.validations.CreatePersonInputDtoValidator"  # noqa
    )
    input_dto_validator_instance = input_dto_validator_mock.return_value
    use_case = use_cases.CreatePersonUseCase(**dependencies)
    request_input = request_models.CreatePersonRequest(
        name=person.name,
        phone=person.phone,
        address=person.address,
        city=person.city,
        country=person.country,
    )
    request_response = response_models.CreatePersonResponse(person_id=person.person_id)
    response = use_case.execute(request_input)

    dependencies["person_repository"].create.assert_called_once()
    input_dto_validator_mock.assert_called_once_with(asdict(request_input))
    input_dto_validator_instance.validate.assert_called_once_with()
    assert response == request_response


def test__create_person_use_case__raises_error__when_person_is_not_created(
    mocker: MockFixture,
    dependencies_factory: Callable[[entities.Person], Dict[str, Any]],
    fixture_person_data: Dict[str, Any],
) -> None:
    person = entities.Person(**fixture_person_data)
    dependencies = dependencies_factory(person)
    dependencies["person_repository"].create.return_value = None
    use_case = use_cases.CreatePersonUseCase(**dependencies)
    request_input = request_models.CreatePersonRequest(
        name=person.name,
        phone=person.phone,
        address=person.address,
        city=person.city,
        country=person.country,
    )

    with pytest.raises(errors.ItemNotCreatedException) as exc_info:
        use_case.execute(request_input)

    assert str(exc_info.value) == f"Person '{person.name}' was not created"


def test__create_person_use_case__raises_error__when_input_data_is_invalid(
    mocker: MockFixture,
    dependencies_factory: Callable[[entities.Person], Dict[str, Any]],
    fixture_person_data: Dict[str, Any],
) -> None:
    person = entities.Person(**fixture_person_data)
    dependencies = dependencies_factory(person)
    use_case = use_cases.CreatePersonUseCase(**dependencies)
    request_input = request_models.CreatePersonRequest(
        name=person.name,
        phone=person.phone,
        address=person.address,
        city="",
        country=person.country,
    )
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(request_input)

    assert str(exc_info.value) == "city: empty values not allowed"
    dependencies["person_repository"].create.assert_not_called()
