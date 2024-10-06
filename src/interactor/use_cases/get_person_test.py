from typing import Any, Callable, Dict, Optional

import pytest
from pytest_mock import MockFixture

from src.domain import entities, interfaces
from src.interactor import errors, request_models, response_models, use_cases


@pytest.fixture
def dependencies_factory(
    mocker: MockFixture,
) -> Callable[[entities.Person], Dict[str, Any]]:
    def _dependencies_factory(
        person: Optional[entities.Person] = None,
    ) -> Dict[str, Any]:
        person_repository_mock = mocker.Mock(interfaces.PersonRepositoryInterface)
        person_repository_mock.get_by_phone.return_value = person
        return {
            "person_repository": person_repository_mock,
        }

    return _dependencies_factory


def test__get_person_by_phone_use_case__returns_a_person__when_successfully(
    mocker: MockFixture,
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[Optional[entities.Person]], Dict[str, Any]],
) -> None:
    person = entities.Person(**fixture_person_data)
    dependencies = dependencies_factory(person)
    use_case = use_cases.GetPersonUseCase(**dependencies)
    request_input = request_models.GetPersonRequest(phone=person.phone)
    request_response = response_models.GetPersonResponse(
        person_id=person.person_id,
        name=person.name,
        phone=person.phone,
        address=person.address,
        city=person.city,
        country=person.country,
    )
    response = use_case.execute(request_input)

    dependencies["person_repository"].get_by_phone.assert_called_once()
    assert response == request_response


def test__get_person_use_case__when_person_is_not_found(
    mocker: MockFixture,
    dependencies_factory: Callable[[Optional[entities.Person]], Dict[str, Any]],
    fixture_person_data: Dict[str, Any],
) -> None:
    dependencies = dependencies_factory(None)
    use_case = use_cases.GetPersonUseCase(**dependencies)
    input_dto = request_models.GetPersonRequest(phone="non_existing_phone_number")

    with pytest.raises(errors.ItemNotFoundException) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == "Person 'non_existing_phone_number' was not found"
    dependencies["person_repository"].get_by_phone.assert_called_once()


def test__get_person_by_id_use_case__returns_a_person__when_successfully(
    mocker: MockFixture,
    fixture_person_data: Dict[str, Any],
    dependencies_factory: Callable[[Optional[entities.Person]], Dict[str, Any]],
) -> None:
    person = entities.Person(**fixture_person_data)
    dependencies = dependencies_factory(person)
    dependencies["person_repository"].get_by_id.return_value = person

    use_case = use_cases.GetPersonUseCase(**dependencies)
    request_input = request_models.GetPersonRequest(person_id=person.person_id)
    request_response = response_models.GetPersonResponse(
        person_id=person.person_id,
        name=person.name,
        phone=person.phone,
        address=person.address,
        city=person.city,
        country=person.country,
    )
    response = use_case.execute(request_input)

    dependencies["person_repository"].get_by_id.assert_called_once_with(
        person.person_id
    )
    assert response == request_response


def test__get_person_by_id_use_case__when_person_is_not_found(
    mocker: MockFixture,
    dependencies_factory: Callable[[Optional[entities.Person]], Dict[str, Any]],
    fixture_person_data: Dict[str, Any],
) -> None:
    dependencies = dependencies_factory(None)
    dependencies["person_repository"].get_by_id.return_value = None
    use_case = use_cases.GetPersonUseCase(**dependencies)
    input_dto = request_models.GetPersonRequest(person_id="non_existing_person_id")

    with pytest.raises(errors.ItemNotFoundException) as exc_info:
        use_case.execute(input_dto)

    assert str(exc_info.value) == "Person 'non_existing_person_id' was not found"
    dependencies["person_repository"].get_by_id.assert_called_once_with(
        "non_existing_person_id"
    )
